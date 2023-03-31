import os
import logging
from datetime import date, timedelta
from services.SmsService import send_sms
from services.WhatsappService import send_to_group
from services.PriceService import get_max_price, get_min_price, get_cheapest_period, format_euro, get_daily_prices
from LoggingConfig import configure_logging
import i18n
from dotenv import load_dotenv

configure_logging()

load_dotenv()

TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS') or ""

i18n.load_path.append('i18n')

today = date.today()
tomorrow = today + timedelta(days=1)

price_data = get_daily_prices(tomorrow)

if not price_data:
    logging.info(
        f'No price data available yet for {tomorrow.strftime("%d %b, %Y")}')
    exit(0)

cheapest_period = get_cheapest_period(price_data, 3)
cheapest_period_avg = format_euro(sum(
    x.value for x in cheapest_period) / len(cheapest_period))

min_price = get_min_price(price_data)
max_price = get_max_price(price_data)

messageEn = i18n.t('text.daily_price',
                   date_time=tomorrow.strftime('%d %b, %Y'),
                   min_price=min_price.formatted,
                   max_price=max_price.formatted,
                   cheapest_period_hour=cheapest_period[0].hour,
                   cheapest_period_value=cheapest_period_avg)

i18n.set('locale', 'es')
messageEs = i18n.t('text.daily_price',
                   date_time=tomorrow.strftime('%d %b, %Y'),
                   min_price=min_price.formatted,
                   max_price=max_price.formatted,
                   cheapest_period_hour=cheapest_period[0].hour,
                   cheapest_period_value=cheapest_period_avg)


logging.info(messageEn)
logging.info(messageEs)

if TWILIO_RECIPIENTS != "":
    for recipient in TWILIO_RECIPIENTS.split(","):
        if recipient.startswith('+34'):
            send_sms(messageEs, recipient)
        else:
            send_sms(messageEn, recipient)

send_to_group(messageEs)
