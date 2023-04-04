import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

GMAIL_SENDER = os.getenv('GMAIL_SENDER')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

if (GMAIL_SENDER == None or GMAIL_APP_PASSWORD == None):
    print('GMAIL_SENDER and GMAIL_APP_PASSWORD must be set in .env')
    exit(1)


def send_email(subject: str, message: str, recipient: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_SENDER
    msg["To"] = recipient

    msg.attach(MIMEText(message.replace("`", "").replace("*", ""), "plain"))

    # Log in to your Gmail account and send the message
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_SENDER, recipient, msg.as_string())

    print(f"Email sent successfully to {recipient}")
