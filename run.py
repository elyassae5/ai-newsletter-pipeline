import subprocess
import sys
import os

BASE = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    ("Scraping sources",        "tools/scrape_sources.py"),
    ("Curating with Claude",    "tools/curate_content.py"),
    ("Drafting newsletter",     "tools/draft_newsletter.py"),
    ("Sending email",           "tools/send_email.py"),
]


def run_step(label, script):
    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"{'='*50}")
    result = subprocess.run(
        [sys.executable, os.path.join(BASE, script)],
        cwd=BASE,
    )
    if result.returncode != 0:
        print(f"\nERROR: '{script}' failed. Stopping pipeline.")
        sys.exit(1)


if __name__ == "__main__":
    print("Starting newsletter pipeline...")
    for label, script in STEPS:
        run_step(label, script)
    print("\nPipeline complete. Newsletter sent.")
