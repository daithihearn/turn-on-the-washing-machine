
import asyncio
from services.PriceService import get_current_price, get_max_price, get_min_price
from services.SmartPlugService import turn_on

curr_price = get_current_price()
min_price = get_min_price()
max_price = get_max_price()


async def main():
    if curr_price.value == min_price.value:
        await turn_on()
    else:
        print('Not turning the smart plug on. Min price is ' +
              min_price.value_euro+', max price is'+max_price.value_euro+', current price is '+curr_price.value_euro+'.')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
