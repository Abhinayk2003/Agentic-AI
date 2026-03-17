import os
import pickle
import re
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/calendar"
]

LAST_EMAILS = []


# ---------------- AUTH ----------------
def authenticate_gmail():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


def get_gmail_service():
    creds = authenticate_gmail()
    return build("gmail", "v1", credentials=creds)


def get_calendar_service():
    creds = authenticate_gmail()
    return build("calendar", "v3", credentials=creds)


def get_connected_email():
    service = get_gmail_service()
    return service.users().getProfile(userId="me").execute()["emailAddress"]


# ---------------- FETCH EMAILS ----------------
def get_emails(query=""):
    global LAST_EMAILS

    service = get_gmail_service()
    user_email = get_connected_email()

    results = service.users().messages().list(
        userId="me",
        q="-in:sent",
        maxResults=10
    ).execute()

    messages = results.get("messages", [])
    LAST_EMAILS = messages

    if not messages:
        return "No emails found."

    output = f"Emails from {user_email}:\n\n"

    for i, msg in enumerate(messages, 1):
        message = service.users().messages().get(
            userId="me", id=msg["id"]
        ).execute()

        headers = message["payload"]["headers"]

        subject, sender = "", ""

        for h in headers:
            if h["name"] == "Subject":
                subject = h["value"]
            if h["name"] == "From":
                sender = h["value"]

        snippet = message.get("snippet", "")

        output += f"{i}. From: {sender}\nSubject: {subject}\nPreview: {snippet}\n\n"

    return output


# ---------------- SEND EMAIL ----------------
def send_email(query):
    service = get_gmail_service()
    sender = get_connected_email()

    to_match = re.search(r"to\s+([\w\.-]+@[\w\.-]+)", query, re.IGNORECASE)
    if not to_match:
        return "Recipient not found"

    to_email = to_match.group(1)

    subject_match = re.search(r"subject\s*:\s*(.*?)(?:body|$)", query, re.IGNORECASE)
    subject = subject_match.group(1).strip() if subject_match else "No Subject"

    body_match = re.search(r"body\s*:\s*(.*)", query, re.IGNORECASE)
    body = body_match.group(1).strip() if body_match else "Hello"

    msg = MIMEText(body)
    msg["to"] = to_email
    msg["from"] = sender
    msg["subject"] = subject

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    service.users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()

    return f"Email sent to {to_email}"


# ---------------- REPLY EMAIL ----------------
def reply_to_email(query):
    global LAST_EMAILS

    if not LAST_EMAILS:
        return "Please fetch emails first"

    service = get_gmail_service()
    sender = get_connected_email()

    index = 0
    if "second" in query:
        index = 1
    elif "third" in query:
        index = 2

    msg_id = LAST_EMAILS[index]["id"]

    message = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="metadata",
        metadataHeaders=["Subject", "From", "Message-ID"]
    ).execute()

    headers = message["payload"]["headers"]

    subject, from_email, message_id = "", "", ""

    for h in headers:
        if h["name"] == "Subject":
            subject = h["value"]
        elif h["name"] == "From":
            from_email = h["value"]
        elif h["name"] == "Message-ID":
            message_id = h["value"]

    email_match = re.search(r"<(.+?)>", from_email)
    to_email = email_match.group(1) if email_match else re.search(r"[\w\.-]+@[\w\.-]+", from_email).group(0)

    msg = MIMEText("Thanks for your email.")
    msg["to"] = to_email
    msg["from"] = sender
    msg["subject"] = f"Re: {subject}"
    msg["In-Reply-To"] = message_id
    msg["References"] = message_id

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw, "threadId": message["threadId"]}
    ).execute()

    return f"Reply sent to {to_email}"


# ---------------- SUMMARIZE ----------------
def summarize_emails(query):
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        q="-in:sent",
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return "No emails found."

    summary = ""
    for msg in messages:
        message = service.users().messages().get(userId="me", id=msg["id"]).execute()
        summary += f"- {message.get('snippet')}\n"

    return "Summary:\n\n" + summary