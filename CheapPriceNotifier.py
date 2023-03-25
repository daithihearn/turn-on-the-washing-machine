import os
from twilio.rest import Client
import requests
import json
from dotenv import load_dotenv

load_dotenv()

PRICES_API = os.getenv('PRICES_API')
TWILIO_ACCOUNT_SSID = os.getenv('TWILIO_ACCOUNT_SSID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM_NUMBER = os.getenv('TWILIO_FROM_NUMBER')
TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS')


def get_current_price():
    # Call the API and get the response
    response = requests.get(PRICES_API+"/now?zone=PCB")
    content = response.content.decode('utf-8')
    data = json.loads(content)

    return data.get('price')


def get_min_price():
    # Call the API and get the response
    response = requests.get(PRICES_API+'/min?zone=PCB')
    content = response.content.decode('utf-8')
    data = json.loads(content)

    return data.get('price')


def send_sms(message):
    client = Client(TWILIO_ACCOUNT_SSID, TWILIO_AUTH_TOKEN)

    for to in TWILIO_RECIPIENTS.split(","):
        client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=to
        )
        print('SMS sent successfully to '+to)


curr_price = get_current_price()
min_price = get_min_price()

if curr_price == min_price:
    send_sms('Put the washing machine on!')
else:
    print('No need to put the washing machine on. Min price is ' +
          str(min_price)+', current price is '+str(curr_price)+'.')
