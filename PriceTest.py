import logging
from datetime import date, timedelta
from services.PriceService import get_prices, calculate_average
from LoggingConfig import configure_logging


configure_logging()

today = date.today()
from_date = today - timedelta(days=30)
to_date = today - timedelta(days=0)

price_data = get_prices(from_date, to_date)

if price_data:
    price_average = calculate_average(price_data)
    logging.info(f'Average: {price_average}')
else:
    logging.info('No data')
