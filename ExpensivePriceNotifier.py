import os
import logging
from services.EmailService import send_email
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import get_current_price, get_today, calculate_average, format_cents_per_kwh
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

average_price = calculate_average(daily_price_info.expensive_period)


def get_subject(locale: str) -> str:
    i18n.set('locale', locale)
    return i18n.t('text.expensive_price_subject')


def get_message(locale: str) -> str:
    i18n.set('locale', locale)
    return i18n.t('text.expensive_price',
                  average_price=format_cents_per_kwh(average_price),
                  period_length=len(daily_price_info.expensive_period))


if curr_price.hour == daily_price_info.expensive_period[0].hour:

    # Get Messages
    message_es = get_message('es')
    subjectEn = get_subject('en')
    message_en = get_message('en')

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
            send_email(subjectEn, message_en, recipient)
else:
    logging.info(
        f'No need to warn about the price. Most expensive period starts at {daily_price_info.expensive_period[0].hour}:00.')
