import feedparser
import json
import os
import re
from datetime import datetime, timezone, timedelta

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../.tmp/raw_articles.json")

FEEDS = [
    {"name": "Hacker News",         "url": "https://news.ycombinator.com/rss"},
    {"name": "MIT Technology Review","url": "https://www.technologyreview.com/feed/"},
    {"name": "The Verge - AI",       "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"},
    {"name": "Ars Technica - AI",    "url": "https://feeds.arstechnica.com/arstechnica/index"},
    {"name": "VentureBeat AI",       "url": "https://venturebeat.com/category/ai/feed/"},
]

HOURS_BACK = 24


def strip_html(text):
    return re.sub(r"<[^>]+>", "", text).strip()


def parse_date(entry):
    for field in ("published_parsed", "updated_parsed"):
        if hasattr(entry, field) and getattr(entry, field):
            t = getattr(entry, field)
            return datetime(*t[:6], tzinfo=timezone.utc)
    return None


def scrape():
    cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS_BACK)
    articles = []

    for feed_info in FEEDS:
        print(f"Fetching: {feed_info['name']}...")
        feed = feedparser.parse(feed_info["url"])

        for entry in feed.entries:
            pub_date = parse_date(entry)
            if pub_date and pub_date < cutoff:
                continue  # too old

            articles.append({
                "title":   entry.get("title", "").strip(),
                "url":     entry.get("link", "").strip(),
                "summary": strip_html(entry.get("summary", ""))[:500],
                "source":  feed_info["name"],
                "date":    pub_date.isoformat() if pub_date else None,
            })

    # deduplicate by url
    seen = set()
    unique = []
    for a in articles:
        if a["url"] not in seen:
            seen.add(a["url"])
            unique.append(a)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {len(unique)} articles saved to {OUTPUT_FILE}")
    return unique


if __name__ == "__main__":
    results = scrape()
    if not results:
        print("WARNING: No articles found. Consider widening HOURS_BACK.")
