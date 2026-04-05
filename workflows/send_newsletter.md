# Workflow: Send Daily AI Newsletter

## Objective
Scrape AI/tech news from RSS feeds, use Claude to curate and summarise the best stories,
render them into a clean HTML email, and send it via Gmail. Run this once per day.

## Required Inputs
- `ANTHROPIC_API_KEY` in `.env`
- `NEWSLETTER_SENDER` in `.env` (your Gmail address)
- `NEWSLETTER_RECIPIENT` in `.env` (who receives the newsletter)
- `credentials.json` in the project root (Google OAuth — one-time setup)

## Steps

### Step 1 — Scrape sources
**Tool:** `tools/scrape_sources.py`
**What it does:** Fetches the last 24 hours of articles from RSS feeds and saves them locally.
**Output:** `.tmp/raw_articles.json`
**Run:** `python tools/scrape_sources.py`

Check that `.tmp/raw_articles.json` exists and contains at least 1 article before proceeding.
If 0 articles found: check if feeds are reachable and if the 24h filter is too strict (widen to 48h).

### Step 2 — Curate with Claude
**Tool:** `tools/curate_content.py`
**What it does:** Sends all raw articles to Claude, which picks the 5–7 best and writes
a short newsletter-style summary for each.
**Input:** `.tmp/raw_articles.json`
**Output:** `.tmp/curated.json`
**Run:** `python tools/curate_content.py`

Check that `.tmp/curated.json` contains between 3 and 7 stories. If Claude returns fewer
than 3, the raw feed may have had low-quality content — widen the sources or time window.
If you hit an API rate limit: wait 60 seconds and retry once before escalating.

### Step 3 — Draft the email
**Tool:** `tools/draft_newsletter.py`
**What it does:** Renders the curated stories into a clean HTML email with subject line,
intro paragraph, story cards, and footer.
**Input:** `.tmp/curated.json`
**Output:** `.tmp/newsletter.html`
**Run:** `python tools/draft_newsletter.py`

Open `.tmp/newsletter.html` in a browser to visually check it looks correct before sending.

### Step 4 — Send via Gmail
**Tool:** `tools/send_email.py`
**What it does:** Reads the HTML email and sends it via Gmail API.
**Input:** `.tmp/newsletter.html`
**Run:** `python tools/send_email.py`

First-time run: a browser window will open for Google OAuth. Complete the flow —
`token.json` will be saved and reused for all future runs automatically.
If authentication fails: delete `token.json` and re-run to re-authenticate.
If send fails: check that the Gmail API is enabled in Google Cloud Console and that
`credentials.json` is valid.

## Edge Cases

| Problem | Fix |
|---|---|
| No articles in last 24h | Widen filter to 48h in `scrape_sources.py` |
| Claude returns < 3 stories | Check raw feed quality, add more sources |
| Gmail OAuth fails | Delete `token.json`, re-run `send_email.py` |
| API rate limit hit | Wait 60s, retry once |
| Email not received | Check spam folder, verify sender/recipient in `.env` |

## Self-Improvement Notes
_Update this section when you discover new constraints, better approaches, or recurring issues._

- (empty — add notes here as you run the workflow)
