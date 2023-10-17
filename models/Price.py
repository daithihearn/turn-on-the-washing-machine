from datetime import datetime
from dataclasses import dataclass, field
from constants import HOUR_FORMAT


@dataclass
class Price:
    id: str
    datetime: datetime
    value: float
    hour: int = field(init=False)

    def __post_init__(self):
        self.hour = self.datetime.strftime(HOUR_FORMAT)
