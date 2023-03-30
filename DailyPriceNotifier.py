import os
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import get_max_price, get_min_price, get_cheapest_period
import i18n
from dotenv import load_dotenv

load_dotenv()

TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS') or ""

i18n.load_path.append('i18n')

cheapest_period = get_cheapest_period(3)
min_price = get_min_price()
max_price = get_max_price()

messageEn = i18n.t('text.daily_price', min_price=str(min_price.value_euro+'@'+min_price.hour),
                   max_price=str(max_price.value_euro+'@'+max_price.hour),
                   cheapest_period_hour=cheapest_period.hour,
                   cheapest_period_value=cheapest_period.value_euro)

i18n.set('locale', 'es')
messageEs = i18n.t('text.daily_price', min_price=str(min_price.value_euro+'@'+min_price.hour),
                   max_price=str(max_price.value_euro+'@'+max_price.hour),
                   cheapest_period_hour=cheapest_period.hour,
                   cheapest_period_value=cheapest_period.value_euro)


print(messageEn)
print(messageEs)

if TWILIO_RECIPIENTS != "":
    for recipient in TWILIO_RECIPIENTS.split(","):
        if recipient.startswith('+34'):
            send_sms(messageEs, recipient)
        else:
            send_sms(messageEn, recipient)

send_to_group(messageEs)
