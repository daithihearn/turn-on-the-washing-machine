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


def get_message(locale: str, min_price: Price, cheapest_periods: tuple[list[Price], list[Price]], expensive_period: list[Price], expensive_period_avg: float, rating: str) -> str:
    i18n.set('locale', locale)

    cheapest_periods_str = ""
    for period in cheapest_periods:
        if period:
            cheapest_periods_str = f'{cheapest_periods_str} {format_euro(calculate_average(period))}@{period[0].hour}:00-{period[2].hour}:59'

    return i18n.t('text.daily_price',
                  date_time=min_price.datetime.strftime('%d %b, %Y'),
                  rating=rating,
                  cheapest_periods=cheapest_periods_str,
                  expensive_period=f'{expensive_period[0].hour}:00-{expensive_period[2].hour}:59',
                  expensive_period_value=format_euro(expensive_period_avg))


def main():
    price_data = get_tomorrow()

    if not price_data:
        logging.info('No price data available yet for tomorrow')
        exit(0)

    median = get_thirty_day_median()

    cheapest_periods = get_two_cheapest_periods(price_data, 3)

    expensive_period = get_most_expensive_period(price_data, 3)
    expensive_period_avg = calculate_average(expensive_period)

    min_price = get_min_price(price_data)

    rating = calculate_day_rating(price_data, median)

    messageEs = get_message('es', min_price, cheapest_periods,
                            expensive_period, expensive_period_avg, rating)
    subjectEn = get_subject('en')
    messageEn = get_message('en', min_price, cheapest_periods,
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
