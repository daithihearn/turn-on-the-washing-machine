import os
import logging
import requests
import json
import babel.numbers
from datetime import date, datetime, timedelta
from dateutil.parser import parse
from dotenv import load_dotenv

load_dotenv()

PRICES_API = os.getenv('PRICES_API')
VARIANCE = 0.02


class Price:
    def __init__(self, price: float, dt: date):
        self.value = price
        self.value_euro = format_euro(price)
        self.datetime = dt
        self.hour = dt.strftime('%H')
        self.formatted = f'{self.value_euro}@{self.hour}:00'


def get_cheap_period_recent_average(days: int) -> float:
    today = date.today()

    total = float(0)
    for i in range(days):
        day = today - timedelta(days=i)
        prices = get_prices(day, day)
        if prices:
            cheapest_period = get_cheapest_period(prices, 3)
            if cheapest_period:
                total += calculate_average(cheapest_period)

    return total / days


def calculate_day_rating(cheapest_period_avg: float) -> str:
    recent_average = get_cheap_period_recent_average(30)
    logging.info(
        f'Recent average: {recent_average} - Tomorrow: {cheapest_period_avg}')

    if (recent_average - cheapest_period_avg) > VARIANCE:
        return "Bueno"
    elif (recent_average - cheapest_period_avg) < -VARIANCE:
        return "Malo"
    else:
        return "Normal"


def get_today():
    today = date.today()
    return get_prices(today, today)


def get_tomorrow():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    return get_prices(tomorrow, tomorrow)


def get_prices(start: date, end: date) -> list[Price]:
    start_day = start.strftime('%Y-%m-%d')
    end_day = end.strftime('%Y-%m-%d')
    response = requests.get(
        f'{PRICES_API}?time_trunc=hour&start_date={start_day}T00:00&end_date={end_day}T23:59')
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

    return min_window


def get_expensive_period(prices: list[Price], n: int):

    prices_sorted = sorted(prices, key=lambda x: x.hour)
    max_sum = float('-inf')
    max_window = None

    for i in range(len(prices_sorted) - n + 1):
        window_sum = sum(x.value for x in prices_sorted[i:i+n])
        if window_sum > max_sum:
            max_sum = window_sum
            max_window = prices_sorted[i:i+n]

    return max_window


def calculate_average(prices: list[Price]) -> float:
    return sum(x.value for x in prices) / len(prices)


def format_euro(amount) -> str:
    return f'{babel.numbers.format_decimal(amount, locale="en_GB")}'
