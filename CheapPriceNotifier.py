import os
import logging
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import get_current_price, get_min_price, get_max_price, get_cheapest_period
from LoggingConfig import configure_logging
import i18n
from dotenv import load_dotenv

configure_logging()

load_dotenv()

TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS')

curr_price = get_current_price()
cheapest_period = get_cheapest_period(3)
min_price = get_min_price()
max_price = get_max_price()

if curr_price.hour == cheapest_period.hour:
    i18n.load_path.append('i18n')
    messageEn = i18n.t('text.cheap_price',
                       min_price=min_price.formatted,
                       max_price=max_price.formatted,
                       cur_price=curr_price.formatted)

    i18n.set('locale', 'es')
    messageEs = i18n.t('text.cheap_price',
                       min_price=min_price.formatted,
                       max_price=max_price.formatted,
                       cur_price=curr_price.formatted)

    for recipient in TWILIO_RECIPIENTS.split(","):
        if recipient.startswith('+34'):
            send_sms(messageEs, recipient)
        else:
            send_sms(messageEn, recipient)

    send_to_group(messageEs)
else:
    logging.info(
        f'No need to put the washing machine on. Cheapest 3 hour period is {cheapest_period.formatted}, min {min_price.formatted}, max {max_price.formatted}, current {curr_price.formatted}.')
