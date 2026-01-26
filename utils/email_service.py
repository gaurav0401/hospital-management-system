import requests

EMAIL_SERVICE_URL = "http://localhost:3000/dev/send-email"



def send_email(action, to_email, data):
    payload = {
        "action": action,
        "to_email": to_email,
        "data": data
    }

    try:
        requests.post(EMAIL_SERVICE_URL, json=payload, timeout=5)
    except Exception:
        pass
