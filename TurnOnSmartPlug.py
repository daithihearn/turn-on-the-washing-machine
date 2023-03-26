
import asyncio
from services.PriceService import get_current_price, get_max_price, get_min_price
from services.SmartPlugService import turn_on

curr_price = get_current_price()
min_price = get_min_price()
max_price = get_max_price()


async def main():
    if curr_price == min_price:
        await turn_on()
    else:
        print('Not turning the smart plug on. Min price is ' +
              min_price.value+', current price is '+curr_price.value+'.')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
