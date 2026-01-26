from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.utils.timezone import make_aware

# def get_calendar_service(user):
#     creds = Credentials(**user.google_token)
#     service = build('calendar', 'v3', credentials=creds)
#     return service
from datetime import datetime

def create_calendar_event(user, title, description, start_dt, end_dt):
    service = get_calendar_service(user)

    if service is None:
        return None  

    start_dt = make_aware(start_dt)
    end_dt = make_aware(end_dt)

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_dt.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_dt.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }

    return service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

def get_calendar_service(user):
    token_data = user.google_token

    if not token_data or not token_data.get("refresh_token"):
        return None  

    creds = Credentials(
        token=token_data["token"],
        refresh_token=token_data["refresh_token"],
        token_uri=token_data["token_uri"],
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"],
        scopes=token_data["scopes"],
    )

    return build("calendar", "v3", credentials=creds)

    
