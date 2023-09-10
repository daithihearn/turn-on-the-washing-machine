import logging
import asyncio
from services.PriceService import get_current_price, get_today, calculate_average
from services.SmartPlugService import turn_on
from LoggingConfig import configure_logging

configure_logging()

today_price_info = get_today()

curr_price = get_current_price(today_price_info.prices)


async def main():
    if curr_price.hour == today_price_info.cheapest_periods.first[0].hour or (len(today_price_info.cheapest_periods.second) > 0 and curr_price.hour == today_price_info.cheapest_periods.second[0].hour):
        await turn_on()
    else:
        logging.info('Not turning the smart plug on.')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
