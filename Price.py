import os
import requests
import json
import babel.numbers
from dotenv import load_dotenv

load_dotenv()

PRICES_API = os.getenv('PRICES_API')


class Price:
    def __init__(self, price, hour):
        self.value = format_euro(price)
        self.hour = str(hour)


def get_current_price() -> Price:
    # Call the API and get the response
    response = requests.get(PRICES_API+"/now?zone=PCB")
    content = response.content.decode('utf-8')
    data = json.loads(content)

    return Price(data.get('price') / 1000, data.get('hour')[0:2]+':00')


def get_min_price():
    # Call the API and get the response
    response = requests.get(PRICES_API+'/min?zone=PCB')
    content = response.content.decode('utf-8')
    data = json.loads(content)

    return Price(data.get('price') / 1000, data.get('hour')[0:2]+':00')


def get_max_price():
    # Call the API and get the response
    response = requests.get(PRICES_API+'/max?zone=PCB')
    content = response.content.decode('utf-8')
    data = json.loads(content)

    return Price(data.get('price') / 1000, data.get('hour')[0:2]+':00')


def format_euro(amount) -> str:
    return babel.numbers.format_currency(amount, 'EUR', locale='en_GB')
