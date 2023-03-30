import os
import pywhatkit
from dotenv import load_dotenv

load_dotenv()
WHATSAPP_GROUP_NAME = os.getenv('WHATSAPP_GROUP_NAME')


def send_to_group(message):
    if WHATSAPP_GROUP_NAME != "":
        print('Sending message to group '+WHATSAPP_GROUP_NAME)
        pywhatkit.sendwhatmsg_to_group_instantly(WHATSAPP_GROUP_NAME, message)
    else:
        print('No group name provided. Skipping sending message to group.')
