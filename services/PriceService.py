import os
import logging
import requests
import json
from babel.numbers import format_decimal
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


def get_thirty_day_median() -> float:
    today = date.today()
    prices = get_prices(today - timedelta(days=30), today)
    return calculate_average(prices)


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


def calculate_day_rating(price_data: list[Price], median: float) -> str:
    curr_median = calculate_average(price_data)
    low_line = median - VARIANCE
    high_line = median + VARIANCE

    logging.info(
        f'Current median: {curr_median} median: {median} low_line: {low_line} high_line: {high_line}')

    if (curr_median < low_line):
        return 'BUENO'
    elif (curr_median >= low_line and curr_median <= high_line):
        return 'NORMAL'
    else:
        return 'MALO'


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
        f'{PRICES_API}?start={start_day}&end={end_day}')
    content = response.content.decode('utf-8')
    price_data = json.loads(content)

    return [Price(x.get('price'), parse(x.get('dateTime'))) for x in price_data]


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


def get_two_cheapest_periods(prices: list[Price], n: int) -> tuple[list[Price], list[Price]]:
    if len(prices) < n:
        return [], []

    first_period = get_cheapest_period(prices, n)

    remaining_prices_before = [
        p for p in prices if p.datetime < first_period[0].datetime]
    remaining_prices_after = [
        p for p in prices if p.datetime > first_period[n - 1].datetime]

    first_period_before = get_cheapest_period(remaining_prices_before, n)
    first_period_after = get_cheapest_period(remaining_prices_after, n)

    if first_period_before and len(first_period_before) == n and first_period_after and len(first_period_after) == n:
        first_period_before_average = calculate_average(first_period_before)
        first_period_after_average = calculate_average(first_period_after)

        second_period = first_period_before if first_period_before_average < first_period_after_average else first_period_after
    else:
        second_period = first_period_before if first_period_before and len(
            first_period_before) == n else first_period_after

    now = datetime.now()
    end_of_first_period = first_period[n - 1].datetime + timedelta(hours=3)
    end_of_second_period = second_period[n - 1].datetime + timedelta(hours=3)

    if end_of_first_period < now:
        first_period = []

    if end_of_second_period < now or end_of_second_period <= end_of_first_period:
        second_period = []

    return first_period, second_period


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
    return f'{format_decimal(amount, locale="en_GB", format="#,##0.000")}'
