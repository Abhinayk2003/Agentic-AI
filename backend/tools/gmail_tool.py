import os
import pickle
import re
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail API Scopes
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar",
]


def authenticate_gmail():
    """Authenticate and return Gmail API service"""
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

    service = build("gmail", "v1", credentials=creds)
    return service


def get_connected_email(service):
    """Return the Gmail account connected to the API"""
    profile = service.users().getProfile(userId="me").execute()
    return profile["emailAddress"]


def get_unread_emails(query: str = ""):
    """Fetch unread emails"""
    service = authenticate_gmail()

    # Identify which Gmail account is being used
    email_account = get_connected_email(service)

    results = service.users().messages().list(
        userId="me",
        labelIds=["UNREAD"],
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return f"No unread emails found in {email_account}"

    output = f"Unread emails in {email_account}:\n\n"

    for i, msg in enumerate(messages, 1):

        message = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()

        headers = message["payload"]["headers"]

        subject = ""
        sender = ""

        for header in headers:
            if header["name"] == "Subject":
                subject = header["value"]

            if header["name"] == "From":
                sender = header["value"]

        snippet = message.get("snippet", "")

        output += (
            f"{i}. From: {sender}\n"
            f"   Subject: {subject}\n"
            f"   Preview: {snippet}\n\n"
        )

    return output


def send_email(query: str):
    """Send an email using Gmail from natural language"""

    service = authenticate_gmail()
    email_account = get_connected_email(service)

    # Extract recipient email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", query)

    if not email_match:
        return "No email address found in your request."

    recipient = email_match.group()

    # Default values
    subject = "Message from AI Assistant"
    body = "Hello"

    # Extract subject
    subject_match = re.search(r"subject[: ](.+?)( body|$)", query, re.IGNORECASE)
    if subject_match:
        subject = subject_match.group(1).strip()

    # Extract body
    body_match = re.search(r"(body|regarding|saying)[: ](.+)", query, re.IGNORECASE)
    if body_match:
        body = body_match.group(2).strip()

    # Create email
    msg = MIMEText(body)
    msg["to"] = recipient
    msg["subject"] = subject

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    message = {"raw": raw}

    service.users().messages().send(
        userId="me",
        body=message
    ).execute()

    return f"Email sent successfully from {email_account} to {recipient}"