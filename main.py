import asyncio
import os
from time import time, sleep
import pymsteams
import logging


from meross_iot.controller.mixins.electricity import ElectricityMixin
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

EMAIL = os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_MAIL"
PASSWORD = os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_PW"
DEVICENAME = os.environ.get('MEROSS_DEVICE_NAME') or "Kaffeemaschine"
WEBHOOK = os.environ.get('TEAMS_WEBHOOK') or "YOUR_TEAMS_WEBHOOK"
MESSAGESTART = os.environ.get('MESSAGE_START') or "Der Kaffee läuft ! Fertig in ca. 15 min."
MESSAGEEND = os.environ.get('MESSAGE_END') or "Der Kaffee ist fertig ! Bitte neuen kochen, wenn er leer ist !"

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


async def main():
    coffeeStatus = False
    while True:
        # Setup the HTTP client API from user-password
        http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

        # Setup and start the device manager
        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()

        # Retrieve all the devices that implement the electricity mixin
        await manager.async_device_discovery()
        devs = manager.find_devices(device_class=ElectricityMixin, device_name=DEVICENAME)

        if len(devs) < 1:
            logging.ERROR("No electricity-capable device found...")
        else:
            dev = devs[0]

            # Update device status: this is needed only the very first time we play with this device (or if the
            #  connection goes down)
            await dev.async_update()

            # Read the electricity power/voltage/current
            instant_consumption = await dev.async_get_instant_metrics()
            logging.INFO(f"Current consumption data: {instant_consumption}")
            if instant_consumption.power == 0.0:
                logging.INFO('Coffemachine is off')
                if coffeeStatus:
                    logging.INFO('Coffe is ready to drink')
                    myTeamsMessage = pymsteams.connectorcard(WEBHOOK)
                    myTeamsMessage.text(MESSAGEEND)
                    myTeamsMessage.send()
                coffeeStatus = False
            else:
                logging.INFO('Coffee Machine is on')
                if not coffeeStatus:
                    logging.INFO('Coffee just got turned on, will be ready in 15 min.')
                    myTeamsMessage = pymsteams.connectorcard(WEBHOOK)
                    myTeamsMessage.text(MESSAGESTART)
                    myTeamsMessage.send()
                coffeeStatus = True

        # Close the manager and logout from http_api
        manager.close()
        await http_api_client.async_logout()
        sleep(60 - time() % 60)


if __name__ == '__main__':
    # On Windows + Python 3.8, you should uncomment the following
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
