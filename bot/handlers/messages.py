import datetime
import logging

from config.configuration import Settings, Constants
from config.config_reader import load_config

from bot.logic import date_converter, search_engine
from bot.db import reminders, users
from bot.handlers.common import register_user
from bot import keyboards

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def create_reminder(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in Settings.blocked_users:
        return await message.answer("🔒 К сожалению вы заблокированны!")

    if message.text.startswith('/'):
        return await message.answer("Такой команды не существует!")

    if not users.get_user_data(str(message.chat.id)):
        return await register_user(message, state)

    time_zone = users.get_user_data(message.chat.id)[5]
    if time_zone == "not_set":
        return await message.answer(Constants.settings_text["please_select_utc"]["ru"], parse_mode="HTML",
                                    reply_markup=keyboards.kb_main_menu)
    text = " ".join(message.text.split())
    date, time, text = search_engine.date_and_time_handling(text, time_zone)

    # обработка ошибок с датой
    if date is None:
        logger.debug("Reminder handling: can not find date in message: {0}".format(message.text))
        return await message.answer("Не удалось обработать дату напоминания!", reply_markup=keyboards.kb_main_menu)

    # проверка корректности даты
    if not date_converter.get_day_of_the_week(date):
        logger.debug("Wrong date input, chat_id: {0}".format(message.chat.id))
        return await message.answer("Некорректная дата!", reply_markup=keyboards.kb_main_menu)

    # обработка ошибок со временем
    if time is None:
        logger.debug("Reminder handling: can not find time in message: {0}".format(message.text))
        return await message.answer(text)

    cur_date = " ".join([date, time])
    reminder_id = reminders.get_free_id(str(message.chat.id))

    # переход к UTS 00:00
    utc_date = date_converter.utc(cur_date, time_zone)

    # проверка на попытку создать напоминание на прошедшее время
    now_date = datetime.datetime.utcnow().strftime(Settings.date_format)
    if date_converter.date_to_value(utc_date) <= date_converter.date_to_value(now_date):
        logger.debug("Trying to create reminder on the past date, chat_id: {0}. Date: {1} Time: {2}".format(
            message.chat.id, date, time))
        return await message.answer("Вы пытаетесь создать напоминание на прошедшее время!", reply_markup=keyboards.kb_main_menu)

    # проверка на отсутствие текста напоминание

    if not text:
        logger.debug("Trying to create reminder without any text, chat_id: {0}".format(message.chat.id))
        return await message.answer("Вы пытаетесь создать напоминание без текста!", reply_markup=keyboards.kb_main_menu)

    users.update_last_reminder(str(message.chat.id), reminder_id)

    # запись напоминания в базу данных и отправка сообщению об успешном создании напоминания
    if reminders.add_new(str(message.chat.id), str(message.message_id), reminder_id, utc_date, text):
        logger.debug("Created reminder for message: {0}\n\t chat_id: {1}, reminder_id: {2}, time: {3}, uts: {4},"
                     "\n\ttext: {5}".format(message.text, message.chat.id, reminder_id, utc_date, time_zone, text))



        # return await message.answer("Уведомление успешно создано.\n"
        #                             f"Дата: <b>{date_converter.get_day_of_the_week(date)} {cur_date}</b>\n"
        #                             f"Id: <b>{reminder_id}</b>\n"
        #                             f"Текст: <b>{text}</b>", parse_mode="HTML", reply_markup=keyboards.kb_main_menu)
        return await message.answer(
            Constants.reminders_format["reminder_created"]["ru"].format(
                day_of_the_week=date_converter.get_day_of_the_week(date),
                cur_date=cur_date,
                reminder_id=reminder_id,
                text=text),
            parse_mode="HTML",
            reply_markup=keyboards.kb_main_menu
        )
    else:
        return await message.answer("Не удалось создать уведомление", reply_markup=keyboards.kb_main_menu)


def register_handlers_messages(dp: Dispatcher):
    dp.register_message_handler(create_reminder, state="*")
