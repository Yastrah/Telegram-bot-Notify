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

# timer_stop.set()
timer_stop = threading.Event()

def timer(bot: Bot, loop):
    asyncio.set_event_loop(loop)

    schedule.every().minute.at(":00").do(lambda: loop.create_task(send_reminders(bot)))

    while not timer_stop.is_set():
        schedule.run_pending()
        sleep(5)


async def send_reminders(bot: Bot):
    now_date = datetime.now().strftime(config.logger.date_format)
    data = data_base.get_now(now_date)

    if data is None:
        logger.debug("Impossible to process reminders - data error.")
        return

    if not data:
        logger.debug("There is no reminders for {0}.".format(now_date))
        return

    logger.debug("There are {0} reminders for {1}.".format(len(data), now_date))

    for message in data:
        try:
            await bot.send_message(chat_id=message["chat_id"], text=message["text"])
        except Exception as e:
            logger.error("Failed to send reminder to user {0}!\n\tException: {1}".format(message["chat_id"], e))
            continue
