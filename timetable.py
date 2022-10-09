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

def timer(bot: Bot):
    # schedule.every().minute.at(":00").do(notification, bot)
    schedule.every().minute.at(":00").do(start_notification, bot)
    # schedule.every().minute.at(":00").do(asyncio.create_task(notification(bot)))
    # schedule.every().day.at("8:00").do(day_plan)
    # schedule.every().day.at("19:00").do(check)


    while not schedule_stop.is_set():
        schedule.run_pending()
        sleep(5)
    # await bot.send_message("1990672413", "some text")


def start_notification(bot: Bot):
    logger.info("start_notification!!!!!!!!!!!!!!!")
    print(asyncio.iscoroutinefunction(notification))
    asyncio.run(notification(bot))


async def notification(bot: Bot):
    now_date = datetime.now().strftime(config.logger.date_format)
    logger.info("NOTIFICATION AT {0}".format(now_date))
    await bot.send_message("1990672413", "some text")

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

