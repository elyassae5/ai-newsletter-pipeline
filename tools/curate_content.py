import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

INPUT_FILE  = os.path.join(os.path.dirname(__file__), "../.tmp/raw_articles.json")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../.tmp/curated.json")


def curate():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)

    if not articles:
        print("ERROR: raw_articles.json is empty. Run scrape_sources.py first.")
        return []

    # Build the article list for the prompt
    article_lines = []
    for i, a in enumerate(articles, 1):
        article_lines.append(
            f"{i}. [{a['source']}] {a['title']}\n   URL: {a['url']}\n   Summary: {a['summary']}"
        )
    articles_text = "\n\n".join(article_lines)

    prompt = f"""You are the editor of a daily AI and tech newsletter.
Below is a list of articles published in the last 24 hours.

Your job:
1. Pick the 5 to 7 most interesting, significant, or useful articles for a technical audience interested in AI and software.
2. For each selected article, write a 2–3 sentence summary in an engaging newsletter tone — concise, informative, no hype.
3. Return ONLY a valid JSON array. No extra text, no markdown, no code fences.

JSON format:
[
  {{
    "title": "original article title",
    "url": "original url",
    "source": "source name",
    "summary": "your 2-3 sentence newsletter summary"
  }}
]

Articles:
{articles_text}"""

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    print(f"Sending {len(articles)} articles to Claude for curation...")
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_response = message.content[0].text.strip()

    try:
        curated = json.loads(raw_response)
    except json.JSONDecodeError:
        # Try to extract JSON array if Claude added any surrounding text
        start = raw_response.find("[")
        end   = raw_response.rfind("]") + 1
        curated = json.loads(raw_response[start:end])

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(curated, f, indent=2, ensure_ascii=False)

    print(f"Done. {len(curated)} stories curated and saved to {OUTPUT_FILE}")
    return curated


if __name__ == "__main__":
    results = curate()
    if len(results) < 3:
        print("WARNING: Fewer than 3 stories curated. Check raw feed quality.")
