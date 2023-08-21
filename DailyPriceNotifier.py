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


def get_message(locale: str, cheapest_periods: tuple[list[Price], list[Price]], expensive_period: list[Price], expensive_period_avg: float, rating: str) -> str:
    i18n.set('locale', locale)

    # If the second cheapest period is empty
    if not cheapest_periods[1]:
        return i18n.t('text.daily_price_one',
                      date_time=expensive_period[0].datetime.strftime(
                          '%d %b, %Y'),
                      rating=rating,
                      period_length=len(cheapest_periods[0]),
                      cheapest_period_one_start=f'{cheapest_periods[0][0].hour}:00',
                      cheapest_period_one_price=format_cents_per_kwh(
                          calculate_average(cheapest_periods[0])),
                      expensive_period_start=f'{expensive_period[0].hour}:00',
                      expensive_period_price=format_cents_per_kwh(expensive_period_avg))

    return i18n.t('text.daily_price_two',
                  date_time=expensive_period[0].datetime.strftime('%d %b, %Y'),
                  rating=rating,
                  cheapest_period_one_start=f'{cheapest_periods[0][0].hour}:00',
                  cheapest_period_one_price=format_cents_per_kwh(
                      calculate_average(cheapest_periods[0])),
                  cheapest_period_two_start=f'{cheapest_periods[1][0].hour}:00',
                  cheapest_period_two_price=format_cents_per_kwh(
                      calculate_average(cheapest_periods[1])),
                  expensive_period_start=f'{expensive_period[0].hour}:00',
                  expensive_period_price=format_cents_per_kwh(expensive_period_avg))


def main():
    price_data = get_tomorrow()

    if not price_data:
        logging.info('No price data available yet for tomorrow')
        exit(0)

    median = get_thirty_day_median()

    cheapest_periods = get_two_cheapest_periods(price_data, 3)

    expensive_period = get_most_expensive_period(price_data, 3)
    expensive_period_avg = calculate_average(expensive_period)

    rating = calculate_day_rating(price_data, median)

    messageEs = get_message('es', cheapest_periods,
                            expensive_period, expensive_period_avg, rating)
    subjectEn = get_subject('en')
    messageEn = get_message('en', cheapest_periods,
                            expensive_period, expensive_period_avg, rating)

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

    write_output_to_file(messageEs)


if not check_output_file():
    main()
else:
    logging.info(
        f"Output file for date {today_date} already exists. Skipping execution.")
