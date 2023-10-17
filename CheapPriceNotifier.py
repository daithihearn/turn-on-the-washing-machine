import os
import logging
from services.EmailService import send_email
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import format_cents_per_kwh, get_current_price, get_today, calculate_average
from LoggingConfig import configure_logging
import i18n
from dotenv import load_dotenv

configure_logging()

load_dotenv()
i18n.load_path.append('i18n')

TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS') or ""
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS') or ""

daily_price_info = get_today()

if not daily_price_info:
    logging.info('No price data available')
    exit(0)

curr_price = get_current_price(daily_price_info.prices)


def get_subject(locale: str) -> str:
    i18n.set('locale', locale)
    return i18n.t('text.cheap_price_subject')


def get_message(locale: str, average_price: str, cheapest_period_length: int) -> str:
    i18n.set('locale', locale)
    return i18n.t('text.cheap_price',
                  period_length=cheapest_period_length,
                  average_price=format_cents_per_kwh(average_price))


def send_message(average_price: str, cheapest_period_length: int):
    # Get Messages
    message_es = get_message('es', average_price, cheapest_period_length)
    subject_en = get_subject('en')
    message_en = get_message('en', average_price, cheapest_period_length)

    logging.info(message_es)
    logging.info(message_en)

    # Send sms to all recipients
    if TWILIO_RECIPIENTS != "":
        for recipient in TWILIO_RECIPIENTS.split(","):
            send_sms(message_es, recipient)

    # Send whatsapp message to all recipients
    send_to_group(message_es)

    # Send email to all recipients
    if EMAIL_RECIPIENTS != "":
        for recipient in EMAIL_RECIPIENTS.split(","):
            send_email(subject_en, message_en, recipient)


logging.info(
    f'Current hour: {curr_price.hour} price: {curr_price.value}')

for period in daily_price_info.cheapest_periods:

    if (len(period) > 0):
        logging.info(
            f'Cheap hour:   {period[0].hour} price: {period[0].value}')
        if (curr_price.hour == period[0].hour):
            send_message(calculate_average(period), len(period))
            exit(0)

logging.info('No need to put the washing machine on.')
