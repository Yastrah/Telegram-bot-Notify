import logging

from config.configuration import Settings

from app.config_reader import load_config
from app.logic import date_converter, search_engine
from app import data_base

from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def create_reminder(message: types.Message):
    text = " ".join(message.text.split())  # избавление от лишних пробелов

    date = None

    found, text = search_engine.search_day_name(text, "сегодня")
    if found:
        date = date_converter.today()

    if date is None:
        found, text = search_engine.search_day_name(text, "завтра")
        if found:
            date = date_converter.tomorrow()

    for day in [day[1] for day in Settings.week_days]:
        found, text = search_engine.search_day_name(text, day)
        if found:
            date = date_converter.nearest_day_of_the_week(day)
            break

    if date is None:
        date, text = search_engine.search_date(text)

    time, text = search_engine.search_time(text)

    if date is None or time is None:
        logger.debug("Reminder handling error!")
        return

    full_date = " ".join([date, time])

    if data_base.add_new(full_date, str(message.chat.id), text):
        logger.debug("Created reminder:\t chat_id: {0}, time: {1}, text: {2}".format(message.chat.id,
                                                                                     full_date, text))

        await message.answer("Уведомление успешно создано.\n"
                             f"Дата: {date_converter.get_day_of_the_week(date)} {full_date}\n"
                             f"Текст: {text}")
    else:
        await message.answer("Не удалось создать уведомление")


def register_handlers_message(dp: Dispatcher):
    dp.register_message_handler(create_reminder, state="*")
    # dp.register_message_handler(cmd_help, commands="help", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
