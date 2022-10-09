import logging
import schedule
import asyncio
import threading
from time import sleep
from datetime import datetime
from aiogram import Bot

from app.config_reader import load_config
from app import data_base


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")

# schedule_stop.set()
# def timer():
#     while not schedule_stop.is_set():
#         schedule.run_pending()
#         sleep(5)

schedule_stop = threading.Event()

def timer(bot: Bot, loop):
    # await bot.send_message("1990672413", "some text")
    last_minute = -1
    asyncio.set_event_loop(loop)
    # loop.run_forever()

    while not schedule_stop.is_set():
        if int(str(datetime.now())[14:16]) > last_minute or int(str(datetime.now())[14:16]) == 0:
            if last_minute == 59:
                last_minute = 0
            else:
                last_minute += 1

            # asyncio.run(send_notifications(bot))
            # loop = asyncio.get_event_loop()
            loop.create_task(send_notifications(bot))
            # print(asyncio.get_event_loop())
            # print(asyncio.get_event_loop().is_running())
            # loop.run_until_complete(send_notifications(bot))
            # asyncio.run(send_notifications(bot))
        sleep(32)



async def send_notifications(bot: Bot):
    now_date = datetime.now().strftime(config.logger.date_format)
    # logger.info("NOTIFICATION AT {0}".format(now_date))
    # await bot.send_message("1990672413", "some text")

    data = data_base.get_now(now_date)

    if data is None:
        logger.debug("Impossible to process notifications - data error.")
        return

    if not data:
        logger.debug("There is no notifications for {0}.".format(now_date))
        return

    logger.debug("There is {0} notifications for {1}.".format(len(data), now_date))

    for message in data:
        logger.info(message)
        await bot.send_message(chat_id=message["chat_id"], text=message["text"])

