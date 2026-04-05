import json
import os
from datetime import datetime

INPUT_FILE  = os.path.join(os.path.dirname(__file__), "../.tmp/curated.json")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../.tmp/newsletter.html")


def draft():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        stories = json.load(f)

    if not stories:
        print("ERROR: curated.json is empty. Run curate_content.py first.")
        return

    today = datetime.now().strftime("%B %d, %Y")
    subject = f"Your AI & Tech Digest — {today}"

    story_cards = ""
    for story in stories:
        story_cards += f"""
        <div style="margin-bottom:32px; padding-bottom:32px; border-bottom:1px solid #e5e7eb;">
            <p style="margin:0 0 4px 0; font-size:12px; color:#6b7280; text-transform:uppercase; letter-spacing:0.05em;">
                {story.get('source', '')}
            </p>
            <h2 style="margin:0 0 10px 0; font-size:18px; font-weight:600; line-height:1.4;">
                <a href="{story['url']}" style="color:#111827; text-decoration:none;">
                    {story['title']}
                </a>
            </h2>
            <p style="margin:0 0 10px 0; font-size:15px; color:#374151; line-height:1.6;">
                {story['summary']}
            </p>
            <a href="{story['url']}" style="font-size:13px; color:#2563eb; text-decoration:none; font-weight:500;">
                Read more →
            </a>
        </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subject}</title>
</head>
<body style="margin:0; padding:0; background-color:#f9fafb; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">

    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f9fafb;">
        <tr>
            <td align="center" style="padding:40px 16px;">

                <!-- Card -->
                <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px; width:100%; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.08);">

                    <!-- Header -->
                    <tr>
                        <td style="background:#111827; padding:32px 40px;">
                            <h1 style="margin:0; color:#ffffff; font-size:22px; font-weight:700; letter-spacing:-0.02em;">
                                AI &amp; Tech Digest
                            </h1>
                            <p style="margin:6px 0 0 0; color:#9ca3af; font-size:13px;">{today}</p>
                        </td>
                    </tr>

                    <!-- Intro -->
                    <tr>
                        <td style="padding:32px 40px 16px 40px;">
                            <p style="margin:0; font-size:15px; color:#374151; line-height:1.6;">
                                Here are today's top stories in AI and technology — curated and summarised for you.
                            </p>
                        </td>
                    </tr>

                    <!-- Stories -->
                    <tr>
                        <td style="padding:16px 40px 8px 40px;">
                            {story_cards}
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background:#f3f4f6; padding:24px 40px; border-top:1px solid #e5e7eb;">
                            <p style="margin:0; font-size:12px; color:#9ca3af; text-align:center;">
                                Generated automatically · {today}
                            </p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>

</body>
</html>"""

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Done. Newsletter drafted and saved to {OUTPUT_FILE}")
    print(f"Subject line: {subject}")
    return subject, html


if __name__ == "__main__":
    draft()
