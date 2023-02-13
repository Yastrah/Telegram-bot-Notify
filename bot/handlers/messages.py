import logging

from config.configuration import Settings, Constants
from config.config_reader import load_config

from bot.logic import date_converter, search_engine
from bot.db import reminders

from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def create_reminder(message: types.Message):
    text = " ".join(message.text.split())

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
        logger.debug("Reminder handling: can not find requirement arguments.")
        return await message.answer("Некорректный формат записи!")

    full_date = " ".join([date, time])
    reminder_id = reminders.get_free_id(str(message.chat.id))

    if reminders.add_new(str(message.chat.id), str(message.message_id), reminder_id, full_date, text):
        logger.debug("Created reminder:\n\t chat_id: {0}, "
                     "reminder_id: {1}, time: {2}, text: {3}".format(message.chat.id, reminder_id, full_date, text))

        await message.answer("Уведомление успешно создано.\n"
                             f"Id: {reminder_id}\n"
                             f"Дата: {date_converter.get_day_of_the_week(date)} {full_date}\n"
                             f"Текст: {text}")
    else:
        await message.answer("Не удалось создать уведомление")


def register_handlers_messages(dp: Dispatcher):
    dp.register_message_handler(create_reminder, state="*")
    # dp.register_message_handler(cmd_help, commands="help", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
