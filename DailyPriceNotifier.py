
from services.SmsService import send_sms
from services.PriceService import get_max_price, get_min_price

min_price = get_min_price()
max_price = get_max_price()

message = 'Prices today:\n  - Min:        '+min_price.value_euro + '@' + \
    min_price.hour + '\n  - Max:       ' + \
    max_price.value_euro + '@' + max_price.hour

print(message)

send_sms(message)
