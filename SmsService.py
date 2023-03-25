import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
TWILIO_ACCOUNT_SSID = os.getenv('TWILIO_ACCOUNT_SSID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM_NUMBER = os.getenv('TWILIO_FROM_NUMBER')
TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS')


def send_sms(message):
    client = Client(TWILIO_ACCOUNT_SSID, TWILIO_AUTH_TOKEN)

    for to in TWILIO_RECIPIENTS.split(","):
        client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=to
        )
        print('SMS sent successfully to '+to)
