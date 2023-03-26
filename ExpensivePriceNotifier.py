
from services.SmsService import send_sms
from services.PriceService import get_current_price, get_max_price, get_min_price

curr_price = get_current_price()
min_price = get_min_price()
max_price = get_max_price()

message = 'Turn everything off!! Now is the most expensive time. Min price: ' + \
    min_price.value_euro + '@' + min_price.hour + ', Max price: ' + max_price.value_euro + '@' + max_price.hour + \
    ', Current Price: ' + curr_price.value_euro + '@' + curr_price.hour + '.'

print(message)

if curr_price.value == max_price.value:
    send_sms(message)
else:
    print('No need to warn about the price. Min price is ' +
          min_price.value_euro+', max price is' + max_price.value_euro+', current price is '+curr_price.value_euro+'.')