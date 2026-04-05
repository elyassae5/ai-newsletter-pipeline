import os
import base64
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

ROOT            = os.path.join(os.path.dirname(__file__), "..")
INPUT_FILE      = os.path.join(ROOT, ".tmp/newsletter.html")
CREDENTIALS_FILE = os.path.join(ROOT, "credentials.json")
TOKEN_FILE      = os.path.join(ROOT, "token.json")
SCOPES          = ["https://www.googleapis.com/auth/gmail.send"]


def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def build_message(sender, recipient, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = sender
    msg["To"]      = recipient
    msg.attach(MIMEText(html_body, "html"))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {"raw": raw}


def send():
    sender    = os.getenv("NEWSLETTER_SENDER")
    recipient = os.getenv("NEWSLETTER_RECIPIENT")

    if not sender or not recipient:
        print("ERROR: NEWSLETTER_SENDER and NEWSLETTER_RECIPIENT must be set in .env")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        html_body = f.read()

    today   = datetime.now().strftime("%B %d, %Y")
    subject = f"Your AI & Tech Digest — {today}"

    print("Authenticating with Gmail...")
    service = get_gmail_service()

    message = build_message(sender, recipient, subject, html_body)

    print(f"Sending to {recipient}...")
    service.users().messages().send(userId="me", body=message).execute()

    print(f"Done. Newsletter sent to {recipient}")


if __name__ == "__main__":
    send()
