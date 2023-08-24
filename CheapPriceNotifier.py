import os
import logging
from services.EmailService import send_email
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import format_cents_per_kwh, get_current_price, get_min_price, get_max_price, get_two_cheapest_periods, get_today, calculate_average
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
cheapest_periods = get_two_cheapest_periods(price_data, 3)
min_price = get_min_price(price_data)
max_price = get_max_price(price_data)


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
    messageEs = get_message('es', average_price, cheapest_period_length)
    subjectEn = get_subject('en')
    messageEn = get_message('en', average_price, cheapest_period_length)

    logging.info(messageEs)
    logging.info(messageEn)

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


if (cheapest_periods[0] and curr_price.hour == cheapest_periods[0][0].hour):
    send_message(calculate_average(
        cheapest_periods[0]), len(cheapest_periods[0]))
elif (cheapest_periods[1] and curr_price.hour == cheapest_periods[1][0].hour):
    send_message(calculate_average(
        cheapest_periods[1]), len(cheapest_periods[0]))
else:
    logging.info('No need to put the washing machine on.')
