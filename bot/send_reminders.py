import logging
import schedule
import asyncio
import threading
from time import sleep
from datetime import datetime
from aiogram import Bot

from config.configuration import Settings
from config.config_reader import load_config
from bot.db import reminders


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")

# timer_stop.set()
timer_stop = threading.Event()

def timer(bot: Bot, loop):
    asyncio.set_event_loop(loop)

    schedule.every().minute.at(":00").do(lambda: loop.create_task(check_for_reminders(bot)))

    while not timer_stop.is_set():
        schedule.run_pending()
        sleep(5)


async def check_for_reminders(bot: Bot):
    now_date = datetime.now().strftime(Settings.date_format)
    data = reminders.get_now(now_date)

    if data is None:
        logger.error("Impossible to process reminders - data error.")
        return

    if not data:
        # logger.debug("There is no reminders for {0}.".format(now_date))
        return

    # logger.debug("There are {0} reminders for {1}.".format(len(data), now_date))

    for reminder in data:
        try:
            await bot.send_message(chat_id=reminder[1], text=reminder[5])
            reminders.remove(id=reminder[0])
            logger.info("Reminder sent successfully to user {0}.\n\tText: {1}".format(reminder[1], reminder[5]))

        except Exception as e:
            logger.error("Failed to send reminder to user {0}!\n\tException: {1}".format(reminder[1], e))
            continue
