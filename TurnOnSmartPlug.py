import logging
import asyncio
from services.PriceService import get_current_price, get_today
from services.SmartPlugService import turn_on, turn_off
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
                f'Cheap period starts at {period[0].hour}:00 and ends at {int(period[-1].hour) + 1}:00')
            if (curr_price.hour == period[0].hour):
                logging.info('Turning the smart plug on.')
                await turn_on()
                exit(0)
            # Else if the current hour is the hour following a cheap period, turn the smart plug off
            elif int(curr_price.hour) == int(period[-1].hour) + 1:
                logging.info('Turning the smart plug off.')
                await turn_off()
                exit(0)
            else:
                logging.info('No need to do anything.')

    exit(0)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
