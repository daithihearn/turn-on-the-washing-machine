import logging
import asyncio
from services.PriceService import get_current_price, get_min_price, get_max_price, get_cheapest_period, get_today, calculate_average
from services.SmartPlugService import turn_on
from LoggingConfig import configure_logging

configure_logging()

price_data = get_today()

if not price_data:
    logging.info('No price data available')
    exit(0)

curr_price = get_current_price(price_data)
cheapest_period = get_cheapest_period(price_data, 3)
min_price = get_min_price(price_data)
max_price = get_max_price(price_data)

cheapest_period_avg = calculate_average(cheapest_period)


async def main():
    if curr_price.hour == cheapest_period[0].hour:
        await turn_on()
    else:
        logging.info(
            f'Not turning the smart plug on. Cheapest 3 hour period starts at {cheapest_period[0].hour}:00, min {min_price.formatted}, max {max_price.formatted}, current {curr_price.formatted}.')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
