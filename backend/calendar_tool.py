
import datetime
import re
import base64
import pytz
from googleapiclient.discovery import build
from email.mime.text import MIMEText

from tools.gmail_tool import authenticate_gmail, get_connected_email


def create_meeting(query: str):
    """Create a Google Calendar meeting and send meeting details via email"""

    # Authenticate Gmail
    service = authenticate_gmail()

    # Build Google Calendar service
    calendar_service = build(
        "calendar",
        "v3",
        credentials=service._http.credentials
    )

    gmail_service = service

    # Extract attendee email from query
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', query)

    if not email_match:
        return "No attendee email found in the request."

    attendee = email_match.group()

    # Use IST timezone
    ist = pytz.timezone("Asia/Kolkata")

    # Meeting time (1 hour from now)
    start_time = datetime.datetime.now(ist) + datetime.timedelta(hours=1)
    end_time = start_time + datetime.timedelta(hours=1)

    # Format time for email display
    start_time_str = start_time.strftime("%d-%m-%Y %I:%M %p")
    end_time_str = end_time.strftime("%d-%m-%Y %I:%M %p")

    # Calendar event payload
    event = {
        "summary": "AI Scheduled Meeting",
        "description": "Meeting created by AI Assistant",
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Asia/Kolkata"
        },
        "attendees": [
            {"email": attendee}
        ]
    }

    # Create Google Calendar event
    event = calendar_service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    meeting_link = event.get("htmlLink")

    # Get sender email
    sender = get_connected_email(service)

    # Email subject
    subject = "Meeting Scheduled"

    # Email body
    body = f"""
Hello,

A meeting has been scheduled.

Meeting Details:

Meeting Link: {meeting_link}

Start Time: {start_time_str}
End Time: {end_time_str}

Please let me know if any changes are required.

With Regards,
Abhinay
"""

    # Create email message
    message = MIMEText(body)
    message["to"] = attendee
    message["from"] = sender
    message["subject"] = subject

    # Encode email
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send email
    gmail_service.users().messages().send(
        userId="me",
        body={"raw": raw_message}
    ).execute()

    return f"Meeting scheduled successfully and email sent to {attendee}"
