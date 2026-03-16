from langchain_core.tools import Tool
import tools
from calendar_tool import create_meeting


# Wrapper for reading emails
def read_unread_emails(input_text: str = ""):
    return tools.get_unread_emails()


# Wrapper for sending email
def send_email_tool(input_text: str):
    try:
        return tools.send_email(input_text)
    except Exception as e:
        return f"Error sending email: {e}"


def generate_tools():

    tools_list = [

        Tool(
            name="GetUnreadEmails",
            func=read_unread_emails,
            description="Fetch unread emails from Gmail"
        ),

        Tool(
            name="SendEmail",
            func=send_email_tool,
            description="Send an email. Example: send email to example@gmail.com subject hello body test message"
        ),

        Tool(
            name="CreateMeeting",
            func=create_meeting,
            description="Schedule a meeting in Google Calendar"
        )

    ]

    return tools_list