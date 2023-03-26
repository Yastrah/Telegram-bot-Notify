import logging
import schedule
import asyncio
import threading
from time import sleep
import datetime
from aiogram import Bot

from config.configuration import Settings
from config.config_reader import load_config
from bot.db import reminders, users, protection


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")

# timer_stop.set()
timer_stop = threading.Event()


def timer(bot: Bot, loop):
    asyncio.set_event_loop(loop)

    schedule.every().minute.at(":00").do(lambda: loop.create_task(check_for_reminders(bot)))
    schedule.every().day.at("00:00").do(protection.checking_for_old_reminders)


    while not timer_stop.is_set():
        schedule.run_pending()
        sleep(5)


async def check_for_reminders(bot: Bot):
    # now_date = datetime.datetime.now().strftime(Settings.date_format)
    now_date = datetime.datetime.utcnow().strftime(Settings.date_format)
    # cur_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).strftime(Settings.date_format)

    data = reminders.get_now(now_date)

    if data is None:
        logger.error("Impossible to process reminders - data error.")
        return

    if not data:
        return

    for reminder in data:
        # try:
        await bot.send_message(chat_id=reminder[1], text=f"🔔 <b>{reminder[5]}</b>", parse_mode="HTML")
        reminders.remove(id=reminder[0])

        users.update_total_reminders(reminder[1])
        if users.get_user_data(reminder[1])[3] == reminder[3]:
            users.update_last_reminder(reminder[1], 0)

        logger.info("Reminder sent successfully to user {0}.\n\tText: {1}".format(reminder[1], reminder[5]))

        # except Exception as e:
        #     logger.error("Failed to send reminder to user {0}!\n\tException: {1}".format(reminder[1], e))
        #     continue
