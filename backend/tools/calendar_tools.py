from tools.gmail_tools import get_calendar_service
import datetime


def create_meeting(query: str):
    service = get_calendar_service()

    start = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    end = start + datetime.timedelta(hours=1)

    event = {
        "summary": "Meeting",
        "start": {"dateTime": start.isoformat() + "Z"},
        "end": {"dateTime": end.isoformat() + "Z"},
    }

    event = service.events().insert(
        calendarId="primary", body=event
    ).execute()

    return f"Meeting created: {event.get('htmlLink')}"