import os
from dotenv import load_dotenv

load_dotenv()

PRICES_API = os.getenv('PRICES_API')
VARIANCE = 0.02
DAY_FORMAT = '%Y-%m-%d'
HOUR_FORMAT = '%H'
TWILIO_RECIPIENTS = os.getenv('TWILIO_RECIPIENTS') or ""
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS') or ""
