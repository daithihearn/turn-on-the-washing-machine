from datetime import datetime
from dataclasses import dataclass, field
from constants import HOUR_FORMAT


@dataclass
class Price:
    datetime: datetime
    value: float
    hour: str = field(init=False)

    def __post_init__(self):
        self.hour = self.datetime.strftime(HOUR_FORMAT)
