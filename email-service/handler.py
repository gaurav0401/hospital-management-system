import json
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "anonymoususerfortesting@gmail.com"
SENDER_PASSWORD = "#$jysdjhasvchja%"  # Gmail App Password

print("EMAIL FUNCTION CALLED")
def send_email(event, context):
    try:
        body = json.loads(event["body"])

        action = body.get("action")
        to_email = body.get("to_email")
        data = body.get("data", {})

        if action == "SIGNUP_WELCOME":
            subject = "Welcome to Mini HMS"
            message = f"""
Hello {data.get('name')},

Welcome to Mini HMS!
Your account has been successfully created.

Regards,
Mini HMS Team
"""

        elif action == "BOOKING_CONFIRMATION":
            subject = "Appointment Confirmed"
            message = f"""
Hello {data.get('name')},

Your appointment is confirmed.

Doctor: {data.get('doctor')}
Date: {data.get('date')}
Time: {data.get('time')}

Thank you,
Mini HMS Team
"""

        else:
            return response(400, "Invalid action")

        send_mail(to_email, subject, message)

        return response(200, "Email sent successfully")

    except Exception as e:
        return response(500, str(e))


def send_mail(to_email, subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
    
    server.quit()


def response(status, message):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": message}),
    }
