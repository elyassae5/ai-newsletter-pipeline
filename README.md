# AI Newsletter Curator

An automated pipeline that scrapes AI & tech news daily, uses Claude AI to curate and summarize the best stories, renders them into a clean HTML email, and sends it via Gmail — fully hands-off.

## How It Works

```
RSS Feeds (5 sources)
      ↓
scrape_sources.py     → fetches articles from the last 24h
      ↓
curate_content.py     → Claude picks the top 5-7 stories, writes summaries
      ↓
draft_newsletter.py   → renders a clean HTML email
      ↓
send_email.py         → sends via Gmail API
```

## Architecture

Built using the **WAT framework** (Workflows, Agents, Tools):

- **Workflows** — markdown SOPs that define what to do step-by-step (`workflows/`)
- **Agents** — Claude handles reasoning and curation
- **Tools** — deterministic Python scripts handle execution (`tools/`)

This separation keeps AI focused on what it's good at (reasoning) while execution stays reliable and testable.

## Tech Stack

- **Python 3.12+**
- **Claude API** (Haiku) — content curation and summarization
- **Gmail API** — email delivery via OAuth2
- **feedparser** — RSS feed parsing
- **n8n** — workflow orchestration and scheduling (self-hosted on VPS)

## Sources

| Source | Feed |
|---|---|
| Hacker News | news.ycombinator.com/rss |
| MIT Technology Review | technologyreview.com/feed |
| The Verge — AI | theverge.com/rss/ai-artificial-intelligence |
| Ars Technica | feeds.arstechnica.com |
| VentureBeat AI | venturebeat.com/category/ai/feed |

## Project Structure

```
├── tools/
│   ├── scrape_sources.py        # Fetch articles from RSS feeds
│   ├── curate_content.py        # Claude API picks + summarizes stories
│   ├── draft_newsletter.py      # Render HTML email template
│   └── send_email.py            # Send via Gmail API (OAuth2)
├── workflows/
│   └── send_newsletter.md       # Step-by-step SOP for the pipeline
├── run.py                       # Single-command pipeline runner
├── requirements.txt             # Pinned dependencies
├── .env.example                 # Environment variable template
└── CLAUDE.md                    # Agent instructions (WAT framework)
```

## Setup

### 1. Clone and install

```bash
git clone https://github.com/elyassae5/ai-newsletter-pipeline.git
cd ai-newsletter-pipeline
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your API key and email addresses:

```
ANTHROPIC_API_KEY=your_key_here
NEWSLETTER_SENDER=your@gmail.com
NEWSLETTER_RECIPIENT=recipient@email.com
```

### 3. Set up Gmail API

1. Create a project in [Google Cloud Console](https://console.cloud.google.com)
2. Enable the **Gmail API**
3. Configure OAuth consent screen (External, add your email as test user)
4. Create OAuth credentials (Desktop app) → download as `credentials.json`
5. Place `credentials.json` in the project root
6. Run `python tools/send_email.py` once to complete the OAuth flow

### 4. Run

```bash
python run.py
```

### 5. Automate (optional)

Deploy to a VPS and schedule with n8n, cron, or any task scheduler to run daily.

## Sample Output

The newsletter arrives as a clean HTML email with:
- Dark header with date
- 5-7 curated story cards with source, title, AI-written summary, and link
- Minimal footer

## License

MIT
