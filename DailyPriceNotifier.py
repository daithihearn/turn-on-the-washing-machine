
from services.SmsService import send_sms
from services.PriceService import get_max_price, get_min_price

min_price = get_min_price()
max_price = get_max_price()

message = 'Prices today: Min price: ' + \
    min_price.value + '@' + min_price.hour + ', Max price: ' + \
    max_price.value + '@' + max_price.hour

print(message)

send_sms(message)
