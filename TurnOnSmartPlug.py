import logging
import asyncio
from services.PriceService import get_current_price, get_today, calculate_average
from services.SmartPlugService import turn_on
from LoggingConfig import configure_logging

configure_logging()

today_price_info = get_today()

curr_price = get_current_price(today_price_info.prices)

logging.info(
    f'Current hour: {curr_price.hour} price: {curr_price.value}')


async def main():
    for period in today_price_info.cheapest_periods:
        if (len(period) > 0):
            logging.info(
                f'Cheap hour:   {period[0].hour} price: {period[0].value}')
            if (curr_price.hour == period[0].hour):
                await turn_on()
                exit(0)

    logging.info('Not turning the smart plug on.')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
