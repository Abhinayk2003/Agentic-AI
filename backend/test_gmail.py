from tools.gmail_tool import get_unread_emails
from googleapiclient.discovery import build
import pickle

# Load token
with open("token.pickle", "rb") as token:
    creds = pickle.load(token)

# Connect to Gmail API
service = build("gmail", "v1", credentials=creds)

# Get connected email account
profile = service.users().getProfile(userId="me").execute()

print("Connected Gmail Account:")
print(profile["emailAddress"])

print("\nUnread Emails:\n")

emails = get_unread_emails()

print(emails)