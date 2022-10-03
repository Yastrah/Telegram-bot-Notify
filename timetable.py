import logging
import schedule
import asyncio
from time import sleep
from datetime import datetime
from aiogram import Bot

from app.config_reader import load_config
from app import data_base


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")

def worker_main(bot: Bot):
    schedule.every().minute.at(":00").do(start_notification, bot)
    # schedule.every().day.at("8:00").do(day_plan)
    # schedule.every().day.at("19:00").do(check)

    while True:
        schedule.run_pending()
        sleep(1)


def start_notification(bot):
    asyncio.run(notification(bot))


async def notification(bot):
    now_date = datetime.now().strftime(config.logger.date_format)

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

