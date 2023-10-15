import os
import logging
from services.EmailService import send_email
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import DailyPriceInfo, format_cents_per_kwh, get_tomorrow, calculate_average
from LoggingConfig import configure_logging
from datetime import datetime
import i18n
from dotenv import load_dotenv

configure_logging()

load_dotenv()

TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS') or ""
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS') or ""

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

    expensive_period_avg = calculate_average(
        price_info.expensive_period)
    # Get day rating text
    if price_info.rating == "GOOD":
        day_rating = i18n.t(
            'text.daily_rating_good', date_time=price_info.expensive_period[0].datetime.strftime('%d %b, %Y'),)
    elif price_info.rating == "NORMAL":
        day_rating = i18n.t(
            'text.daily_rating_normal', date_time=price_info.expensive_period[0].datetime.strftime('%d %b, %Y'),)
    else:
        day_rating = i18n.t(
            'text.daily_rating_bad', date_time=price_info.expensive_period[0].datetime.strftime('%d %b, %Y'),)

    # If the second cheapest period is empty
    if not price_info.cheapest_periods.second:
        return day_rating + i18n.t('text.daily_price_one',
                                   cheapest_period_one_start=f'{price_info.cheapest_periods.first[0].hour}:00',
                                   cheapest_period_one_end=f'{price_info.cheapest_periods.first[-1].hour}:59',
                                   cheapest_period_one_price=format_cents_per_kwh(
                                       calculate_average(price_info.cheapest_periods.first)),
                                   expensive_period_start=f'{price_info.expensive_period[0].hour}:00',
                                   expensive_period_end=f'{price_info.expensive_period[-1].hour}:59',
                                   expensive_period_price=format_cents_per_kwh(expensive_period_avg))

    return day_rating + i18n.t('text.daily_price_two',
                               cheapest_period_one_start=f'{price_info.cheapest_periods.first[0].hour}:00',
                               cheapest_period_one_end=f'{price_info.cheapest_periods.first[-1].hour}:59',
                               cheapest_period_one_price=format_cents_per_kwh(
                                   calculate_average(price_info.cheapest_periods.first)),
                               cheapest_period_two_start=f'{price_info.cheapest_periods.second[0].hour}:00',
                               cheapest_period_two_end=f'{price_info.cheapest_periods.second[-1].hour}:59',
                               cheapest_period_two_price=format_cents_per_kwh(
                                   calculate_average(price_info.cheapest_periods.second)),
                               expensive_period_start=f'{price_info.expensive_period[0].hour}:00',
                               expensive_period_end=f'{price_info.expensive_period[-1].hour}:59',
                               expensive_period_price=format_cents_per_kwh(expensive_period_avg))


def main():
    try:
        tomorrow_price_info = get_tomorrow()

        message_es = get_message('es', tomorrow_price_info)
        subject_en = get_subject('en')
        message_en = get_message('en', tomorrow_price_info)

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
else:
    logging.info(
        f"Output file for date {today_date} already exists. Skipping execution.")
