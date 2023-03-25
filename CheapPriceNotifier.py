
from SmsService import send_sms
from Price import get_current_price, get_max_price, get_min_price

curr_price = get_current_price()
min_price = get_min_price()
max_price = get_max_price()

message = 'Put the washing machine on! Min price: ' + \
    min_price.value + '@' + min_price.hour + ', Max price: ' + max_price.value + '@' + max_price.hour + \
    ', Current Price: ' + curr_price.value + '@' + curr_price.hour + '.'

print(message)

if curr_price == min_price:
    send_sms(message)
else:
    print('No need to put the washing machine on. Min price is ' +
          min_price.value+', current price is '+curr_price.value+'.')
