
from services.SmsService import send_sms
from services.PriceService import get_current_price, get_max_price, get_min_price

curr_price = get_current_price()
min_price = get_min_price()
max_price = get_max_price()

if curr_price.value == min_price.value:
    send_sms('Put the washing machine on! Min price: ' +
             min_price.value_euro + '@' + min_price.hour + ', Max price: ' + max_price.value_euro + '@' + max_price.hour +
             ', Current Price: ' + curr_price.value_euro + '@' + curr_price.hour + '.')
else:
    print('No need to put the washing machine on. Min price is ' +
          min_price.value_euro+', max price is' + max_price.value_euro+', current price is '+curr_price.value_euro+'.')
