import datetime
import logging

from config.configuration import Settings, Constants
from config.config_reader import load_config

from bot.logic import date_converter, search_engine
from bot.db import reminders, users
from bot.handlers.common import register_user

from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def create_reminder(message: types.Message):
    if message.chat.id in Settings.blocked_users:
        return await message.answer("К сожалению вы заблокированны!")

    text = " ".join(message.text.split())

    date = None

    # поиск и обработка ключевых слов
    found, text = search_engine.search_day_name(text, "сегодня")
    if found:
        date = date_converter.today()

    if date is None:
        found, text = search_engine.search_day_name(text, "завтра")
        if found:
            date = date_converter.tomorrow()

    # поиск и обработка дней недели
    for day in [day[1] for day in Settings.week_days]:
        found, text = search_engine.search_day_name(text, day)
        if found:
            date = date_converter.nearest_day_of_the_week(day)
            break

    # поиск даты в числовом виде, если не нашлось ключевых слов
    if date is None:
        date, text = search_engine.search_date(text)

    # обработка ошибок с датой
    if date is None:
        logger.debug("Reminder handling: can not find date in message: {0}".format(message.text))
        return await message.answer("Не удалось обработать дату напоминания!")

    # поиск времени
    time, text = search_engine.search_time(text)

    # обработка ошибок с датой
    if time is None:
        logger.debug("Reminder handling: can not find time in message: {0}".format(message.text))
        return await message.answer(text)

    full_date = " ".join([date, time])
    reminder_id = reminders.get_free_id(str(message.chat.id))

    # проверка корректности даты
    if not date_converter.get_day_of_the_week(date):
        logger.debug("Wrong date input, chat_id: {0}".format(message.chat.id))
        return await message.answer("Некорректная дата!")

    # проверка на попытку создать напоминание на прошедшее время
    now_date = datetime.datetime.now().strftime(Settings.date_format)
    if date_converter.date_to_value(" ".join([date, time])) <= date_converter.date_to_value(now_date):
        logger.debug("Trying to create reminder on the past date, chat_id: {0}".format(message.chat.id))
        return await message.answer("Вы пытаетесь создать напоминание на прошедшее время!")

    # проверка на отсутствие текста напоминание
    if not text:
        logger.debug("Trying to create reminder without any text, chat_id: {0}".format(message.chat.id))
        return await message.answer("Вы пытаетесь создать напоминание без текста!")

    if not users.get_user_data(str(message.chat.id)):
        await register_user(message)

    users.update_last_reminder(str(message.from_user.id), reminder_id)

    # запись напоминания в базу данных и отправка сообщению об успешном создании напоминания
    if reminders.add_new(str(message.chat.id), str(message.message_id), reminder_id, full_date, text):
        logger.debug("Created reminder for message: {0}\n\t chat_id: {1}, "
                     "reminder_id: {2}, time: {3}, text: {4}".format(message.text, message.chat.id, reminder_id, full_date, text))



        return await message.answer("Уведомление успешно создано.\n"
                             f"Дата: <b>{date_converter.get_day_of_the_week(date)} {full_date}</b>\n"
                             f"Id: <b>{reminder_id}</b>\n"
                             f"Текст: <b>{text}</b>", parse_mode="HTML")
    else:
        return await message.answer("Не удалось создать уведомление")


def register_handlers_messages(dp: Dispatcher):
    dp.register_message_handler(create_reminder, state="*")
