import logging
import time
from services.EmailService import send_email
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import get_current_price, get_today, calculate_average, format_cents_per_kwh
from LoggingConfig import configure_logging
from constants import TWILIO_RECIPIENTS, EMAIL_RECIPIENTS
import i18n
from typing import List
from models.Price import Price

configure_logging()

i18n.load_path.append('i18n')

daily_price_info = get_today()

if not daily_price_info:
    logging.info('No price data available')
    exit(0)

curr_price = get_current_price(daily_price_info.prices)


def get_subject(locale: str) -> str:
    i18n.set('locale', locale)
    return i18n.t('text.expensive_price_subject')


def get_message(locale: str, period: List[Price]) -> str:
    i18n.set('locale', locale)
    message_start = i18n.t('text.expensive_price')
    message_period = i18n.t('text.daily_price_item', period_start=f'{period[0].hour}:00', period_end=f'{period[-1].hour}:59', period_price=format_cents_per_kwh(
        calculate_average(period)))
    message_link = i18n.t('text.link')

    return message_start + message_period + message_link


def send_message(period: List[Price]) -> None:
    # Get Messages
    message_es = get_message('es', period)
    subject_en = get_subject('en')
    message_en = get_message('en', period)

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
    f'Current hour:   {curr_price.hour} price: {curr_price.value}')

for period in daily_price_info.expensive_periods:
    if (len(period) > 0):
        logging.info(
            f'Expensive hour: {period[0].hour} price: {period[0].value}')
        if (curr_price.hour == period[0].hour):
            send_message(period)
            time.sleep(10)
            exit(0)

logging.info('No need to warn about the price')
