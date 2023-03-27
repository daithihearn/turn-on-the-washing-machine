import os
from services.SmsService import send_sms
from services.PriceService import get_max_price, get_min_price
import i18n
from dotenv import load_dotenv

load_dotenv()

TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS')

i18n.load_path.append('i18n')

min_price = get_min_price()
max_price = get_max_price()

messageEn = i18n.t('text.daily_price', min_price=str(min_price.value_euro +
                                                     '@'+min_price.hour), max_price=str(max_price.value_euro+'@'+max_price.hour))

i18n.set('locale', 'es')
messageEs = i18n.t('text.daily_price', min_price=str(min_price.value_euro +
                                                     '@'+min_price.hour), max_price=str(max_price.value_euro+'@'+max_price.hour))

for recipient in TWILIO_RECIPIENTS.split(","):
    if recipient.startswith('+34'):
        send_sms(messageEs, recipient)
    else:
        send_sms(messageEn, recipient)
