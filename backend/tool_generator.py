from langchain_core.tools import Tool
from tools.gmail_tools import (
    get_emails,
    send_email,
    reply_to_email,
    summarize_emails
)
from tools.calendar_tools import create_meeting


def generate_tools():
    return [
        Tool("GetEmails", get_emails, "Fetch emails"),
        Tool("SendEmail", send_email, "Send email"),
        Tool("ReplyEmail", reply_to_email, "Reply emails"),
        Tool("SummarizeEmails", summarize_emails, "Summarize emails"),
        Tool("CreateMeeting", create_meeting, "Schedule meeting")
    ]