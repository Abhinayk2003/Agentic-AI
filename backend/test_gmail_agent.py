import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "tools"))

from tool_generator import generate_tools
# Initialize tools
tools = generate_tools()
get_emails = next(t for t in tools if t.name == "GetUnreadEmails").func
send_email = next(t for t in tools if t.name == "SendEmail").func

# ------------------------------
# Test 1: Show all unread emails
print("===== Test 1: All Unread Emails =====")
print(get_emails("show unread emails"))

# ------------------------------
# Test 2: Show unread emails on a specific date
test_date = "15-03-2026"
print(f"\n===== Test 2: Unread Emails on {test_date} =====")
print(get_emails(f"show unread emails on {test_date}"))

# ------------------------------
# Test 3: Count unread emails on a specific date
print(f"\n===== Test 3: Count Unread Emails on {test_date} =====")
print(get_emails(f"how many unread emails on {test_date}"))

# ------------------------------
# Test 4: Show unread emails from a specific sender
test_sender = "apollo@example.com"
print(f"\n===== Test 4: Unread Emails from {test_sender} =====")
print(get_emails(f"show unread emails from {test_sender}"))

# ------------------------------
# Test 5: Send an email automatically based on topic
test_email = "abc@gmail.com"
topic = "Artificial Intelligence"
print(f"\n===== Test 5: Send Email about {topic} =====")
print(send_email(f"send email to {test_email} about {topic}"))

# ------------------------------
# Test 6: Create a draft email
draft_topic = "Project Updates"
print(f"\n===== Test 6: Create Draft Email about {draft_topic} =====")
print(send_email(f"create draft to {test_email} about {draft_topic}"))
