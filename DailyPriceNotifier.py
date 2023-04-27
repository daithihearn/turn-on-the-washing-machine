import os
import logging
from services.EmailService import send_email
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import *
from LoggingConfig import configure_logging
import i18n
from dotenv import load_dotenv

configure_logging()

load_dotenv()

TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS') or ""
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS') or ""

i18n.load_path.append('i18n')

price_data = get_tomorrow()

if not price_data:
    logging.info('No price data available yet for tomorrow')
    exit(0)

median = get_thirty_day_median()

cheapest_period = get_cheapest_period(price_data, 3)
cheapest_period_avg = calculate_average(cheapest_period)

expensive_period = get_expensive_period(price_data, 3)
expensive_period_avg = calculate_average(expensive_period)

min_price = get_min_price(price_data)
max_price = get_max_price(price_data)


rating = calculate_day_rating(price_data, median)


def get_subject(locale: str) -> str:
    i18n.set('locale', locale)
    return i18n.t('text.daily_price_subject')


def get_message(locale: str) -> str:
    i18n.set('locale', locale)
    return i18n.t('text.daily_price',
                  date_time=min_price.datetime.strftime('%d %b, %Y'),
                  rating=rating,
                  cheapest_period=f'{cheapest_period[0].hour}:00-{cheapest_period[2].hour}:59',
                  cheapest_period_value=format_euro(cheapest_period_avg),
                  expensive_period=f'{expensive_period[0].hour}:00-{expensive_period[2].hour}:59',
                  expensive_period_value=format_euro(expensive_period_avg))


messageEs = get_message('es')
subjectEn = get_subject('en')
messageEn = get_message('en')

logging.info(messageEs)
logging.info(messageEn)

# Send SMS to all recipients
if TWILIO_RECIPIENTS != "":
    for recipient in TWILIO_RECIPIENTS.split(","):
        send_sms(messageEs, recipient)

# Send WhatsApp to group
send_to_group(messageEs)

# Send email to all recipients
if EMAIL_RECIPIENTS != "":
    for recipient in EMAIL_RECIPIENTS.split(","):
        send_email(subjectEn, messageEn, recipient)
