import pytz
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def get_timezone():
    return pytz.timezone('Europe/Madrid')


def parse_isoformat(iso_str):
    tz = "Europe/Madrid"
    # If the string ends with 'Z', replace it with '+00:00'
    if iso_str.endswith('Z'):
        iso_str = iso_str[:-1] + '+00:00'
    return datetime.fromisoformat(iso_str).replace(
        tzinfo=timezone.utc).astimezone(ZoneInfo(tz))


def increment_or_wrap(value: str):
    if value == "23":
        return 0
    else:
        return int(value) + 1
