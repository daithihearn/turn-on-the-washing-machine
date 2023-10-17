from datetime import datetime
from typing import List
from enum import Enum
from dataclasses import dataclass, field
from .DayRating import DayRating
from .Price import Price


@dataclass
class DailyPriceInfo:
    day_rating: DayRating
    thirty_day_average: float
    prices: List[Price]
    cheapest_periods: List[List[Price]]
    expensive_periods: List[List[Price]]
