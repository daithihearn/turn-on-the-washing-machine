import os
import pywhatkit
from dotenv import load_dotenv

load_dotenv()
WHATSAPP_GROUP_NAME = os.getenv('WHATSAPP_GROUP_NAME')


def send_to_group(message):
    pywhatkit.sendwhatmsg_to_group_instantly(WHATSAPP_GROUP_NAME, message)
