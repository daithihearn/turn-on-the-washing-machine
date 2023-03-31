import logging
import asyncio
from services.PriceService import get_current_price, get_min_price, get_max_price, get_cheapest_period
from services.SmartPlugService import turn_on
from LoggingConfig import configure_logging

configure_logging()

curr_price = get_current_price()
cheapest_period = get_cheapest_period(3)
min_price = get_min_price()
max_price = get_max_price()


async def main():
    if curr_price.hour == cheapest_period.hour:
        await turn_on()
    else:
        logging.info(
            f'Not turning the smart plug on. Cheapest 3 hour period {cheapest_period.formatted}, min {min_price.formatted}, max {max_price.formatted}, current {curr_price.formatted}.')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
