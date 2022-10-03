import logging
import threading
# import asyncio
# import emoji
# import datetime

from app.config_reader import load_config
from app.handlers.message import register_handlers_message

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from timetable import worker_main


version = "1.0.1"

logger = logging.getLogger(__name__)


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(dispatcher: Dispatcher):
    commands = [
        BotCommand(command=f"/start", description="начать"),
        BotCommand(command=f"/help", description="помощь в использовании"),
        BotCommand(command=f"/today", description="список дел на сегодня"),
    ]
    await dispatcher.bot.set_my_commands(commands)
    logger.info("Bot commands have been set.")


async def on_startup(dispatcher):
    await set_commands(dispatcher)

    th = threading.Thread(target=worker_main, args=[dispatcher.bot])
    th.start()
    logger.info("Start schedule process.")


def main():
    config = load_config("config/bot.ini")

    logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=config.logger.level,
                        datefmt="%Y-%m-%d %H:%M:%S")

    bot = Bot(token=config.bot.token)
    dp = Dispatcher(bot)

    logger.info(f"VERSION: {version}")

    register_handlers_message(dp)
    # register_handlers_team(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


# from time import sleep
# import datetime
# import schedule
# i = 0
#
#
# def schedule_test():
#     print("Start: {0}".format(datetime.datetime.now()))
#     # schedule.every(10).seconds.do(job)
#     schedule.every().minute.at(":00").do(check)
#     # schedule.every().minute.at(":30").do(check)
#     schedule.every().day.at("19:00").do(check)
#
#     while 1:
#         schedule.run_pending()
#         sleep(1)
#
# def check():
#     # import requests
#     # data = requests.get('https://openexchangerates.org/api/latest.json?app_id=5afbdb5b639a415e84ca3be39f76c605&base=USD&symbols=RUB').json()
#     # print(data['rates']['RUB'])
#
#     print("Check at {1}".format(i, datetime.datetime.now()))
#
#
# def Re():
#     from app import date_converter
#     import re
#     # import regex
#     config = load_config("config/bot.ini")
#
#     # message = "1/10 13:30 сделать уроки до 15:20."
#     message = "заВтра  14  сделать уроки до 19:20."
#     # message = "завтра  14  сделать уроки до 19:20."
#     # message = "33.09.20 13:30 сделать уроки до 15:20."
#     # message = "c 30/09/22 ..dfsf"
#
#     print(f"Исходное сообщение:\n{message}")
#     message = " ".join(message.split())
#     print("--------------------------------\n")
#
#
#     tomorrow_pattern = re.compile("завтра", re.IGNORECASE)
#
#     match = tomorrow_pattern.search(message)
#
#     if match and match.start() <= 7:
#         print("дата найдена: {0}".format(match.group()))
#
#         message = " ".join(message.replace(match.group(), '', 1).split())  # сообщение без даты
#         print(message, '\n')
#
#         now_date = datetime.datetime.now().strftime(config.logger.date_format)
#         date = date_converter.tomorrow(now_date).split()[0]
#         print("дата обработана: {0}".format(date))
#
#     else:
#         # date_pattern = re.compile("(\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4})")
#         date_pattern = re.compile("\d{1,2}([-./]\d{1,2})?([-./]\d{2,4})?")
#
#         match = date_pattern.search(message)
#
#         if match and match.start() <= 7:
#
#             print("дата найдена: {0}".format(match.group()))
#             date = re.split(r"[-./]", match.group())
#
#             message = " ".join(message.replace(match.group(), '', 1).split())  # сообщение без даты
#             print(message, '\n')
#
#             now_date = datetime.datetime.now().strftime(config.logger.date_format)
#             now_date = now_date.split()[0].split('/')
#
#             for num in date:
#                 if len(num) == 1:
#                     date[date.index(num)] = f"0{num}"
#                 elif len(num) > 2:
#                     print("ERROR")
#
#             for i in range(len(date), 3):
#                 date.append(now_date[i])
#
#             if len(date[2]) == 2:
#                 date[2] = now_date[2][:2] + date[2]
#
#             date = "/".join(date)
#
#             print("дата обработана: {0}".format(date))
#
#
#     # ---Поиск времени--- #
#     print("--------------------------------\n")
#     time_pattern = re.compile("\d{1,2}([:. /]\d{1,2})?")
#
#     match = time_pattern.search(message)
#
#     if match and match.start() <= 4:
#         if len(match.group().split(':')) == 1:
#             time = f"{match.group()}:00:00"
#         elif len(match.group().split(':')) == 2:
#             time = f"{match.group()}:00"
#         else:
#             time = match.group()
#
#         print("время обработано: {0}".format(time))
#
#         message = " ".join(message.replace(match.group(), '', 1).split())  # сообщение без времени
#         print(message, '\n')
#
#
#     print("--------------------------------\n")
#     now_date = datetime.datetime.now().strftime(config.logger.date_format)
#     print("Текущая дата: {0}\n".format(now_date))
#     # print(date_converter.tomorrow(now_date))
#
#
#     full_date = " ".join([date, time])
#     print("Дата напоминания: {0}".format(full_date))
#     print("Текст напоминания: {0}".format(message))





if __name__ == "__main__":
    from app import data_base
    data_base.reset()
    main()
    # Re()