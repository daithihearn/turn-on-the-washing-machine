import os
import logging
from services.EmailService import send_email
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import get_current_price, get_max_price, get_min_price, get_today
from LoggingConfig import configure_logging
import i18n
from dotenv import load_dotenv

configure_logging()

load_dotenv()
i18n.load_path.append('i18n')

TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS') or ""
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS') or ""

price_data = get_today()

if not price_data:
    logging.info('No price data available')
    exit(0)

curr_price = get_current_price(price_data)
min_price = get_min_price(price_data)
max_price = get_max_price(price_data)


def get_subject(locale: str) -> str:
    i18n.set('locale', locale)
    return i18n.t('text.expensive_price_subject')


def get_message(locale: str) -> str:
    i18n.set('locale', locale)
    return i18n.t('text.expensive_price',
                  min_price=min_price.formatted,
                  max_price=max_price.formatted,
                  cur_price=curr_price.formatted)


messageEs = get_message('es')
subjectEn = get_subject('en')
messageEn = get_message('en')

logging.info(messageEs)
logging.info(messageEn)

if curr_price.hour == max_price.hour:

    # Send sms to all recipients
    if TWILIO_RECIPIENTS != "":
        for recipient in TWILIO_RECIPIENTS.split(","):
            send_sms(messageEs, recipient)

    # Send whatsapp message to all recipients
    send_to_group(messageEs)

    # Send email to all recipients
    if EMAIL_RECIPIENTS != "":
        for recipient in EMAIL_RECIPIENTS.split(","):
            send_email(subjectEn, messageEn, recipient)
else:
    logging.info(
        f'No need to warn about the price. Min {min_price.formatted}, max {max_price.formatted}, current {curr_price.formatted}.')
