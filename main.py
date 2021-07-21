import asyncio
import datetime
import os
from time import time, sleep
import pymsteams
import logging

from meross_iot.controller.mixins.electricity import ElectricityMixin
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Brew

EMAIL = os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_MAIL"
PASSWORD = os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_PW"
DEVICENAME = os.environ.get('MEROSS_DEVICE_NAME') or "Kaffeemaschine"
WEBHOOK = os.environ.get('TEAMS_WEBHOOK') or "YOUR_TEAMS_WEBHOOK"
MESSAGESTART = os.environ.get('MESSAGE_START') or "Der Kaffee läuft ! Fertig in ca. 15 min."
MESSAGEEND = os.environ.get('MESSAGE_END') or "Der Kaffee ist fertig ! Bitte neuen kochen, wenn er leer ist !"
SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL') or "postgresql://postgres:coffee@localhost/coffee"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


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
            logging.error("No electricity-capable device found...")
        else:
            dev = devs[0]

            # Update device status: this is needed only the very first time we play with this device (or if the
            #  connection goes down)
            await dev.async_update()

            # Read the electricity power/voltage/current
            instant_consumption = await dev.async_get_instant_metrics()
            logging.info(f"Current consumption data: {instant_consumption}")
            if instant_consumption.power == 0.0:
                logging.info('Coffemachine is off')
                if coffeeStatus:
                    logging.info('Coffe is ready to drink')
                    Session = sessionmaker(bind=engine)
                    session = Session()
                    to_create = Brew(startOrStop=False, created_date=datetime.datetime.utcnow())
                    session.add(to_create)
                    session.commit()
                    session.close()
                    myTeamsMessage = pymsteams.connectorcard(WEBHOOK)
                    myTeamsMessage.text(MESSAGEEND)
                    myTeamsMessage.send()
                coffeeStatus = False
            else:
                logging.info('Coffee Machine is on')
                if not coffeeStatus:
                    logging.info('Coffee just got turned on, will be ready in 15 min.')
                    Session = sessionmaker(bind=engine)
                    session = Session()
                    to_create = Brew(startOrStop=True, created_date=datetime.datetime.utcnow())
                    session.add(to_create)
                    session.commit()
                    session.close()
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
