import logging
import os
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from dotenv import load_dotenv

load_dotenv()

MEROSS_EMAIL = os.getenv('MEROSS_EMAIL')
MEROSS_PASSWORD = os.getenv('MEROSS_PASSWORD')
DEVICE_TO_TURN_ON = os.getenv('DEVICE_TO_TURN_ON')


async def turn_on():
    if (DEVICE_TO_TURN_ON != None):
        # Setup the HTTP client API from user-password
        http_api_client = await MerossHttpClient.async_from_user_password(email=MEROSS_EMAIL, password=MEROSS_PASSWORD)
        # Setup and start the device manager
        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()

        # Retrieve all the MSS310 devices that are registered on this account
        await manager.async_device_discovery()
        plugs = manager.find_devices(device_type="mss310")

        for plug in plugs:
            if (plug.name == DEVICE_TO_TURN_ON):
                logging.info(f'Turning on {plug.name}')
                await plug.async_turn_on(channel=0)


async def turn_off():
    if (DEVICE_TO_TURN_ON != None):
        # Setup the HTTP client API from user-password
        http_api_client = await MerossHttpClient.async_from_user_password(email=MEROSS_EMAIL, password=MEROSS_PASSWORD)
        # Setup and start the device manager
        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()

        # Retrieve all the MSS310 devices that are registered on this account
        await manager.async_device_discovery()
        plugs = manager.find_devices(device_type="mss310")

        for plug in plugs:
            if (plug.name == DEVICE_TO_TURN_ON):
                logging.info(f'Turning off {plug.name}')
                await plug.async_turn_off(channel=0)
