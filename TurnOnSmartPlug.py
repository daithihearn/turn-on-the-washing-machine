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
    if curr_price.value == cheapest_period.value:
        await turn_on()
    else:
        logging.info(
            f'Not turning the smart plug on. Cheapest 3 hour period starts with {cheapest_period.value_euro}, min price is {min_price.value_euro}, max price is {max_price.value_euro}, current price is {curr_price.value_euro}.')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
