import os
import pickle
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

# Gmail API scopes
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]


def get_unread_emails(max_results=5):

    service = get_gmail_service()

    # Get the Gmail account connected
    profile = service.users().getProfile(userId="me").execute()
    email_address = profile["emailAddress"]

    print("Connected Gmail Account:", email_address)

    results = service.users().messages().list(
        userId="me",
        q="is:unread",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    output = f"Connected Gmail: {email_address}\n\n"

    for msg in messages:
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

        output += f"From: {sender}\nSubject: {subject}\n\n"

    return output

def get_connected_email():
    """
    Get the Gmail account connected to the API
    """
    service = get_gmail_service()
    profile = service.users().getProfile(userId="me").execute()
    return profile["emailAddress"]


def get_unread_emails(max_results=5):
    """
    Fetch unread emails from Gmail
    """
    service = get_gmail_service()

    # Get connected email ID
    profile = service.users().getProfile(userId="me").execute()
    email_address = profile["emailAddress"]

    results = service.users().messages().list(
        userId="me",
        q="is:unread",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return f"No unread emails in {email_address}"

    output = f"Unread emails in {email_address}:\n\n"

    for i, msg in enumerate(messages, start=1):

        message = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()

        headers = message["payload"].get("headers", [])

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


def send_email(to_email, subject, body):
    """
    Send an email using Gmail API
    """
    service = get_gmail_service()

    message = MIMEText(body)
    message["to"] = to_email
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    message_body = {"raw": raw_message}

    sent_message = service.users().messages().send(
        userId="me",
        body=message_body
    ).execute()

    return f"Email sent successfully! Message ID: {sent_message['id']}"


# Test section
if __name__ == "__main__":

    print("Connected Gmail:", get_connected_email())

    print("\nFetching unread emails...\n")

    emails = get_unread_emails()

    print(emails)