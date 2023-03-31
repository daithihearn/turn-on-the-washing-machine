import os
import logging
from datetime import date
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import get_current_price, get_max_price, get_min_price, get_daily_prices
from LoggingConfig import configure_logging
import i18n
from dotenv import load_dotenv

configure_logging()

load_dotenv()

TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS')

today = date.today()

price_data = get_daily_prices(today)

if not price_data:
    logging.info(
        f'No price data available yet for {today.strftime("%d %b, %Y")}')
    exit(0)

curr_price = get_current_price(price_data)
min_price = get_min_price(price_data)
max_price = get_max_price(price_data)

if curr_price.hour == max_price.hour:
    i18n.load_path.append('i18n')
    messageEn = i18n.t('text.expensive_price',
                       min_price=min_price.formatted,
                       max_price=max_price.formatted,
                       cur_price=curr_price.formatted)

    i18n.set('locale', 'es')
    messageEs = i18n.t('text.expensive_price',
                       min_price=min_price.formatted,
                       max_price=max_price.formatted,
                       cur_price=curr_price.formatted)

    logging.info(messageEn)
    logging.info(messageEs)

    if TWILIO_RECIPIENTS != "":
        for recipient in TWILIO_RECIPIENTS.split(","):
            if recipient.startswith('+34'):
                send_sms(messageEs, recipient)
            else:
                send_sms(messageEn, recipient)

    send_to_group(messageEs)
else:
    logging.info(
        f'No need to warn about the price. Min {min_price.formatted}, max {max_price.formatted}, current {curr_price.formatted}.')
