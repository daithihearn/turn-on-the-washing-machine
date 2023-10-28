import os
import logging
import time
from models.DayRating import DayRating
from services.EmailService import send_email
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import DailyPriceInfo, format_cents_per_kwh, get_tomorrow, get_today, calculate_average
from LoggingConfig import configure_logging
from datetime import datetime, date, timedelta
from constants import TWILIO_RECIPIENTS, EMAIL_RECIPIENTS
import i18n

configure_logging()

i18n.load_path.append('i18n')

output_file_format = "outputs/output_{}.txt"
today_date = datetime.now().strftime("%Y-%m-%d")


def check_output_file():
    output_filename = output_file_format.format(today_date)
    return os.path.isfile(output_filename)


def write_output_to_file(output):
    output_filename = output_file_format.format(today_date)
    with open(output_filename, 'w') as f:
        f.write(output)


def get_subject(locale: str) -> str:
    i18n.set('locale', locale)
    return i18n.t('text.daily_price_subject')


def get_message(locale: str, price_info: DailyPriceInfo) -> str:
    i18n.set('locale', locale)

    today = date.today()
    tomorrow = (today + timedelta(days=1)).strftime('%d %b, %Y')

    message = ''

    # Get day rating text
    if price_info.day_rating == DayRating.GOOD:
        message = i18n.t(
            'text.daily_rating_good', date_time=tomorrow,)
    elif price_info.day_rating == DayRating.NORMAL:
        message = i18n.t(
            'text.daily_rating_normal', date_time=tomorrow,)
    elif price_info.day_rating == DayRating.BAD:
        message = i18n.t(
            'text.daily_rating_bad', date_time=tomorrow,)
    else:
        logging.error(
            f"Invalid day rating: {price_info.day_rating}. Exiting.")
        exit(1)

    link = i18n.t('text.link')

    if bool(price_info.cheapest_periods):
        message = message + i18n.t('text.daily_price_cheap')
        for period in price_info.cheapest_periods:
            message = message + i18n.t('text.daily_price_item', period_start=f'{period[0].hour}:00', period_end=f'{period[-1].hour}:59', period_price=format_cents_per_kwh(
                calculate_average(period)))
    else:
        message = message + i18n.t('text.daily_price_no_cheap')

    if bool(price_info.expensive_periods):
        message = message + i18n.t('text.daily_price_expensive')
        for period in price_info.expensive_periods:
            message = message + i18n.t('text.daily_price_item', period_start=f'{period[0].hour}:00', period_end=f'{period[-1].hour}:59', period_price=format_cents_per_kwh(
                calculate_average(period)))
    else:
        message = message + i18n.t('text.daily_price_no_expensive')

    return message + link


def main():
    try:
        tomorrow_price_info = get_today()

        message_es = get_message('es', tomorrow_price_info)
        subject_en = get_subject('en')
        message_en = get_message('en', tomorrow_price_info)

        print(message_es)
        print(message_en)

        # Send SMS to all recipients
        if TWILIO_RECIPIENTS != "":
            for recipient in TWILIO_RECIPIENTS.split(","):
                send_sms(message_es, recipient)

        # Send WhatsApp to group
        send_to_group(message_es)

        # Send email to all recipients
        if EMAIL_RECIPIENTS != "":
            for recipient in EMAIL_RECIPIENTS.split(","):
                send_email(subject_en, message_en, recipient)

        write_output_to_file(message_es)
    except Exception as e:
        if e.response.status_code == 404:
            print("No price data available yet for tomorrow")
        else:
            print(f"An error occurred: {e.response.status_code}")


if not check_output_file():
    main()
    time.sleep(10)
else:
    logging.info(
        f"Output file for date {today_date} already exists. Skipping execution.")
