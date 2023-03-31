import os
import logging
import requests
import json
import babel.numbers
from datetime import date, datetime
from dateutil.parser import parse
from dotenv import load_dotenv

load_dotenv()

PRICES_API = os.getenv('PRICES_API')


class Price:
    def __init__(self, price: float, dt: date):
        self.value = price
        self.value_euro = format_euro(price)
        self.datetime = dt
        self.hour = dt.strftime('%H:%M')
        self.formatted = f'{self.value_euro}@{self.hour}'


def get_daily_prices(dt: date):
    day = dt.strftime('%Y-%m-%d')
    response = requests.get(
        f'{PRICES_API}?time_trunc=hour&start_date={day}T00:00&end_date={day}T23:59')
    content = response.content.decode('utf-8')
    data = json.loads(content)
    included = data.get('included')
    if included is None:
        return []

    pvpc = [x for x in included if x.get('id') == '1001']

    if not pvpc:
        return []

    attributes = pvpc[0].get('attributes')

    if attributes is None:
        return []
    price_data = attributes.get('values')

    return [Price(x.get('value') / 1000, parse(x.get('datetime'))) for x in price_data]


def get_current_price(prices: list[Price]) -> Price:
    now = datetime.now()
    hour = now.strftime('%H')
    return next((x for x in prices if x.datetime.strftime('%H') == hour), None)


def get_min_price(prices: list[Price]):
    return min(prices, key=lambda x: x.value)


def get_max_price(prices: list[Price]):
    return max(prices, key=lambda x: x.value)


def get_cheapest_period(prices: list[Price], n: int):

    prices_sorted = sorted(prices, key=lambda x: x.hour)
    min_sum = float('inf')
    min_window = None

    for i in range(len(prices_sorted) - n + 1):
        window_sum = sum(x.value for x in prices_sorted[i:i+n])
        if window_sum < min_sum:
            min_sum = window_sum
            min_window = prices_sorted[i:i+n]

    for val in min_window:
        logging.info(val.formatted)
    return min_window


def format_euro(amount) -> str:
    return babel.numbers.format_currency(amount, 'EUR', locale='en_GB')
