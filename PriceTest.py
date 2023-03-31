import os
import logging
from datetime import date, timedelta
from services.PriceService import get_daily_prices
from LoggingConfig import configure_logging


configure_logging()

today = date.today()
tomorrow = today + timedelta(days=1)

price_data = get_daily_prices(today)

for price in price_data:
    logging.info(f'{price.formatted} {price.datetime}')
