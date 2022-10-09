import logging
import re
import datetime

from app.config_reader import load_config
from app import data_base
from app import date_converter

from aiogram import Dispatcher, types

logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def create_notification(message: types.Message):
    text = " ".join(message.text.split())

    tomorrow_pattern = re.compile("завтра", re.IGNORECASE)
    match = tomorrow_pattern.search(text)

    if match and match.start() <= 7:
        text = " ".join(text.replace(match.group(), '', 1).split())  # сообщение без даты

        now_date = datetime.datetime.now().strftime(config.logger.date_format)
        date = date_converter.tomorrow(now_date).split()[0]

    else:
        date_pattern = re.compile("\d{1,2}([-./]\d{1,2})?([-./]\d{2,4})?")
        match = date_pattern.search(text)

        if match and match.start() <= 7:
            date = re.split(r"[-./]", match.group())
            text = " ".join(text.replace(match.group(), '', 1).split())  # сообщение без даты

            now_date = datetime.datetime.now().strftime(config.logger.date_format)
            now_date = now_date.split()[0].split('/')

            for num in date:
                if len(num) == 1:
                    date[date.index(num)] = f"0{num}"
                elif len(num) > 2:
                    logger.debug("Notification handling error!")

            for i in range(len(date), 3):
                date.append(now_date[i])

            if len(date[2]) == 2:
                date[2] = now_date[2][:2] + date[2]

            date = "/".join(date)

        else:
            logger.debug("Notification handling error!")
            return

    time_pattern = re.compile("\d{1,2}([:. /]\d{1,2})?")
    match = time_pattern.search(text)

    if match and match.start() <= 4:
        if len(match.group().split(':')) == 1:
            time = f"{match.group()}:00:00"
        elif len(match.group().split(':')) == 2:
            time = f"{match.group()}:00"
        else:
            time = match.group()

        text = " ".join(text.replace(match.group(), '', 1).split())  # сообщение без времени

    else:
        logger.debug("Notification handling error!")
        return

    full_date = " ".join([date, time])

    if data_base.add_new(full_date, str(message.chat.id), text):
        logger.debug("Created notification:\t chat_id: {0}, time: {1}, text: {2}".format(full_date,
                                                                                         message.chat.id, text))

        await message.answer("Уведомление успешно создано.\n"
                             f"Дата: {full_date}\n"
                             f"Текст: {text}")
    else:
        await message.answer("Неудалось создать уведомление")


def register_handlers_message(dp: Dispatcher):
    dp.register_message_handler(create_notification, state="*")
    # dp.register_message_handler(cmd_help, commands="help", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
