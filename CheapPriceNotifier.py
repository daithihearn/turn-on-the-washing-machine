import os
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import get_current_price, get_min_price, get_max_price, get_cheapest_period
import i18n
from dotenv import load_dotenv

load_dotenv()

TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS')

curr_price = get_current_price()
cheapest_period = get_cheapest_period(3)
min_price = get_min_price()
max_price = get_max_price()

if curr_price.value == cheapest_period.value:
    i18n.load_path.append('i18n')
    messageEn = i18n.t('text.cheap_price',
                       min_price=str(min_price.value_euro+'@'+min_price.hour),
                       max_price=str(max_price.value_euro+'@'+max_price.hour),
                       cur_price=str(curr_price.value_euro+'@'+curr_price.hour))

    i18n.set('locale', 'es')
    messageEs = i18n.t('text.cheap_price',
                       min_price=str(min_price.value_euro+'@'+min_price.hour),
                       max_price=str(max_price.value_euro+'@'+max_price.hour),
                       cur_price=str(curr_price.value_euro+'@'+curr_price.hour))

    for recipient in TWILIO_RECIPIENTS.split(","):
        if recipient.startswith('+34'):
            send_sms(messageEs, recipient)
        else:
            send_sms(messageEn, recipient)

    send_to_group(messageEs)
else:
    print('No need to put the washing machine on. Cheapest 3 hour period starts with '+cheapest_period.value_euro+', min price is ' +
          min_price.value_euro+', max price is ' + max_price.value_euro+', current price is '+curr_price.value_euro+'.')