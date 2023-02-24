import datetime
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from config.config_reader import load_config
from config.configuration import Constants, Settings
from bot.logic import date_converter, search_engine
from bot.db import reminders
from bot import keyboards


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


class EditReminder(StatesGroup):
    waiting_for_id = State()
    waiting_for_edit_type = State()
    waiting_for_new_data = State()


async def cmd_edit(message: types.Message):
    data = reminders.get_user_reminders(message.chat.id)
    if not data:
        return await message.answer("У вас нет напоминаний, чтобы их изменить")

    await message.answer("Введите id напоминания:", reply_markup=keyboards.kb_cancel)
    await EditReminder.waiting_for_id.set()


async def id_received(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Некорректный id!\nВведите id напоминания:")

    if not int(message.text) in [el[3] for el in reminders.get_user_reminders(message.chat.id)]:
        return await message.answer("Напоминания с id {reminder_id} не существует!\nВведите id напоминания:".format(
            reminder_id=int(message.text)), reply_markup=keyboards.kb_cancel)

    await state.update_data(reminder_id=int(message.text))
    await EditReminder.next()

    reminder = [el for el in reminders.get_user_reminders(message.chat.id) if el[3] == int(message.text)][0]

    await message.answer(f"Дата: <b>{date_converter.get_day_of_the_week(reminder[4].split()[0])} {reminder[4]}</b>\n"
                         f"Id: <b>{reminder[3]}</b>\n"
                         f"Текст: <b>{reminder[5]}</b>\n"
                         f"Что вы хотите изменить?", parse_mode="HTML", reply_markup=keyboards.inline_kb_edit_type)


async def edit_time(call: types.CallbackQuery, state: FSMContext):
    await EditReminder.next()
    await state.update_data(edit_type="time")
    return await call.message.answer("Введите новые время и дату без текста напоминания:")


async def edit_text(call: types.CallbackQuery, state: FSMContext):
    await EditReminder.next()
    await state.update_data(edit_type="text")
    return await call.message.answer("Введите новый текст напоминания:")


async def edit_all(call: types.CallbackQuery, state: FSMContext):
    await EditReminder.next()
    await state.update_data(edit_type="all")
    return await call.message.answer("Введите дату, время и текст напоминания, как при создании нового:")


async def edit_reminder(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data["edit_type"] == "time":
        text = " ".join(message.text.split())
        date, time, text = search_engine.date_and_time_handling(text)
        full_date = " ".join([date, time])

        # проверка корректности даты
        if not date_converter.get_day_of_the_week(date):
            logger.debug("Wrong date input, chat_id: {0}".format(message.chat.id))
            return await message.answer("Некорректная дата!")

        # проверка на попытку создать напоминание на прошедшее время
        now_date = datetime.datetime.now().strftime(Settings.date_format)
        if date_converter.date_to_value(" ".join([date, time])) <= date_converter.date_to_value(now_date):
            logger.debug("Trying to update reminder date on the past, chat_id: {0}".format(message.chat.id))
            return await message.answer("Вы пытаетесь изменить время напоминания на прошедшее!")

        if reminders.edit_time(message.chat.id, data["reminder_id"], full_date):
            logger.debug("Successfully updated reminder date with chat_id: {0}, reminder_id: {1}. New date: {2}".format(
                message.chat.id, data["reminder_id"], full_date))
            await state.finish()
            return await message.answer("Время напоминания успешно изменено", reply_markup=keyboards.kb_main_menu)

        else:
            logger.error("Update date error, chat_id: {0}, text: {1}!".format(message.chat.id, message.text))
            await state.finish()
            return await message.answer("Возникла какая-то ошибка!", reply_markup=keyboards.kb_main_menu)

    elif data["edit_type"] == "text":
        if reminders.edit_text(message.chat.id, data["reminder_id"], message.text):
            logger.debug("Successfully updated reminder text with chat_id: {0}, reminder_id: {1}. New text: {2}".format(
                message.chat.id, data["reminder_id"], message.text))
            await state.finish()
            return await message.answer("Текст напоминания успешно изменён", reply_markup=keyboards.kb_main_menu)

        else:
            logger.error("Update text error, chat_id: {0}, text: {1}!".format(message.chat.id, message.text))
            await state.finish()
            return await message.answer("Возникла какая-то ошибка!", reply_markup=keyboards.kb_main_menu)

    elif data["edit_type"] == "all":
        text = " ".join(message.text.split())
        date, time, text = search_engine.date_and_time_handling(text)
        full_date = " ".join([date, time])

        # проверка корректности даты
        if not date_converter.get_day_of_the_week(date):
            logger.debug("Wrong date input, chat_id: {0}".format(message.chat.id))
            return await message.answer("Некорректная дата!")

        # проверка на попытку создать напоминание на прошедшее время
        now_date = datetime.datetime.now().strftime(Settings.date_format)
        if date_converter.date_to_value(" ".join([date, time])) <= date_converter.date_to_value(now_date):
            logger.debug("Trying to update reminder date on the past, chat_id: {0}".format(message.chat.id))
            return await message.answer("Вы пытаетесь изменить время напоминания на прошедшее!")

        if reminders.edit_all(message.chat.id, data["reminder_id"], full_date, text):
            logger.debug("Successfully updated reminder date and text with chat_id: {0}, reminder_id: {1}. "
                         "New date: {2}; new text {3}".format(
                message.chat.id, data["reminder_id"], full_date, text))
            await state.finish()
            return await message.answer("Время напоминания успешно изменено", reply_markup=keyboards.kb_main_menu)

        else:
            logger.error("Update text error, chat_id: {0}, text: {1}!".format(message.chat.id, message.text))
            await state.finish()
            return await message.answer("Возникла какая-то ошибка!", reply_markup=keyboards.kb_main_menu)

    else:
        logger.error("Error with states for edit reminder, chat_id: {0}!".format(message.chat.id))
        return await message.answer("Возникла какая-то ошибка!", reply_markup=keyboards.kb_main_menu)


def register_handlers_edit(dp: Dispatcher):
    dp.register_message_handler(cmd_edit, commands="edit", state="*")
    dp.register_message_handler(cmd_edit, Text(equals=Constants.user_commands["edit"]["custom_name"]), state="*")
    dp.register_message_handler(id_received, state=EditReminder.waiting_for_id)
    dp.register_callback_query_handler(edit_time, text="time", state=EditReminder.waiting_for_edit_type)
    dp.register_callback_query_handler(edit_text, text="text", state=EditReminder.waiting_for_edit_type)
    dp.register_callback_query_handler(edit_all, text="all", state=EditReminder.waiting_for_edit_type)
    dp.register_message_handler(edit_reminder, state=EditReminder.waiting_for_new_data)
