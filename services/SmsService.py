import os
import logging
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
TWILIO_ACCOUNT_SSID = os.getenv('TWILIO_ACCOUNT_SSID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM_NUMBER = os.getenv('TWILIO_FROM_NUMBER')


def send_sms(message, recipient):
    client = Client(TWILIO_ACCOUNT_SSID, TWILIO_AUTH_TOKEN)

    client.messages.create(
        body=message.replace("`", "").replace("*", ""),
        from_=TWILIO_FROM_NUMBER,
        to=recipient
    )
    logging.info(f'SMS sent successfully to {recipient}')
