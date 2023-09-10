import os
import requests
import json
from typing import List
from babel.numbers import format_decimal
from datetime import date, datetime, timedelta
from dateutil.parser import parse
from dotenv import load_dotenv

load_dotenv()

PRICES_API = os.getenv('PRICES_API')
VARIANCE = 0.02
DAY_FORMAT = '%Y-%m-%d'
HOUR_FORMAT = '%H'


class Price:
    def __init__(self, id: str, dateTime: str, price: float):
        self.value = price
        self.datetime = parse(dateTime)
        self.hour = self.datetime.strftime(HOUR_FORMAT)


class CheapestPeriods:
    def __init__(self, first, second):
        self.first = [Price(**x) for x in first]
        self.second = [Price(**x) for x in second]


class DailyPriceInfo:
    def __init__(self, dayRating, thirtyDayAverage, prices, cheapestPeriods, expensivePeriod):
        self.rating = dayRating
        self.thirty_day_average = thirtyDayAverage
        self.prices = [Price(**x) for x in prices]
        self.cheapest_periods = CheapestPeriods(**cheapestPeriods)
        self.expensive_period = [Price(**x) for x in expensivePeriod]


def get_prices(start: date, end: date) -> list[Price]:
    start_day = start.strftime(DAY_FORMAT)
    end_day = end.strftime(DAY_FORMAT)
    response = requests.get(
        f'{PRICES_API}?start={start_day}&end={end_day}')
    response.raise_for_status()
    content = response.content.decode('utf-8')
    price_data = json.loads(content)

    return [Price(**x) for x in price_data]


def get_daily_price_info(datetime: date) -> DailyPriceInfo:
    day = datetime.strftime(DAY_FORMAT)
    response = requests.get(f'{PRICES_API}/dailyinfo?date={day}')
    response.raise_for_status()
    content = response.content.decode('utf-8')
    daily_info_data = json.loads(content)

    return DailyPriceInfo(**daily_info_data)


def get_today() -> DailyPriceInfo:
    today = date.today()
    return get_daily_price_info(today)


def get_tomorrow() -> DailyPriceInfo:
    today = date.today()
    tomorrow = today + timedelta(days=1)
    return get_daily_price_info(tomorrow)


def get_current_price(prices: list[Price]) -> Price:
    now = datetime.now()
    hour = now.strftime(HOUR_FORMAT)
    return next((x for x in prices if x.datetime.strftime(HOUR_FORMAT) == hour), None)


def get_min_price(prices: list[Price]):
    return min(prices, key=lambda x: x.value)


def get_max_price(prices: list[Price]):
    return max(prices, key=lambda x: x.value)


def calculate_average(prices: list[Price]) -> float:
    return sum(x.value for x in prices) / len(prices)


def format_euro(amount) -> str:
    return f'{format_decimal(amount, locale="en_GB", format="#,##0.00")}'


def format_cents_per_kwh(amount) -> str:
    return f'{round(amount * 100)}'


def sort_prices_by_date(prices: List[Price]) -> List[Price]:
    return sorted(prices, key=lambda p: p.datetime)
