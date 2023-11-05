import os
import requests
import json
from typing import List
from babel.numbers import format_decimal
from datetime import date, datetime, timedelta, timezone
from dateutil.parser import parse
from dotenv import load_dotenv
from models.DailyPriceInfo import DailyPriceInfo
from models.Price import Price
from models.DayRating import DayRating
from constants import PRICES_API, DAY_FORMAT, HOUR_FORMAT


def json_to_daily_price_info(json_str: str) -> DailyPriceInfo:
    data = json.loads(json_str)

    # Convert the 'prices' list of dictionaries to a list of 'Price' objects
    prices = [Price(datetime=datetime.fromisoformat(
        p['dateTime']), value=p['price']) for p in data['prices']]

    # Convert the 'cheapestPeriods' and 'expensivePeriods' lists of lists of dictionaries
    cheapest_periods = [
        [
            Price(
                datetime=datetime.fromisoformat(p['dateTime'].replace(
                    'Z', '')).replace(tzinfo=timezone.utc),
                value=p['price']
            ) for p in period
        ] for period in data['cheapestPeriods']]
    expensive_periods = [
        [
            Price(
                datetime=datetime.fromisoformat(p['dateTime'].replace(
                    'Z', '')).replace(tzinfo=timezone.utc),
                value=p['price']
            ) for p in period
        ] for period in data['expensivePeriods']
    ]

    # Convert the 'dayRating' string to the 'DayRating' enum
    day_rating = DayRating(data['dayRating'])

    return DailyPriceInfo(
        day_rating=day_rating,
        thirty_day_average=data['thirtyDayAverage'],
        prices=prices,
        cheapest_periods=cheapest_periods,
        expensive_periods=expensive_periods
    )


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

    return json_to_daily_price_info(content)


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
    return next((x for x in prices if x.hour == hour), None)


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
