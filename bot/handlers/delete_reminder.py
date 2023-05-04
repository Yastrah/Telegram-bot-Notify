import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from config.config_reader import load_config
from config.configuration import Constants, Settings
from bot.logic import date_converter
from bot.db import reminders, users
from bot import keyboards

logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


class DeleteReminder(StatesGroup):
    waiting_for_id = State()
    waiting_for_confirm = State()


async def cmd_delete(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in Settings.blocked_users:
        return await message.answer("🔒 К сожалению вы заблокированны!")

    data = reminders.get_user_reminders(message.chat.id)
    if not data:
        return await message.answer("⚡️ У вас нет напоминаний, чтобы их удалить")

    id_list = [x[3] for x in data]

    await message.answer("Выберите id напоминания:", reply_markup=keyboards.inline_kb_id_list(id_list))
    await message.answer("Или введите id вручную:", reply_markup=keyboards.kb_cancel)
    await DeleteReminder.waiting_for_id.set()


async def cmd_undo(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in Settings.blocked_users:
        return await message.answer("🔒 К сожалению вы заблокированны!")

    data = users.get_user_data(message.chat.id)
    user_reminders = reminders.get_user_reminders(message.chat.id)

    if data[3] == 0:
        return await message.answer("⚡️ Последнее созданное напоминание удалено или уже отправлено")

    if not user_reminders:
        users.update_last_reminder(message.chat.id, 0)
        return await message.answer("⚡️ Последнее созданное напоминание удалено или уже отправлено")

    await state.update_data(reminder_id=data[3])

    await DeleteReminder.waiting_for_confirm.set()

    reminder = [el for el in user_reminders if el[3] == data[3]]
    if reminder:
        reminder = reminder[0]
    else:
        logger.error(
            "Last_reminder_id has given, but there is no such reminder. User_id: {0}".format(message.from_user.id))
        users.update_last_reminder(message.chat.id, 0)
        return await message.answer("⚡️Последнее созданное напоминание удалено или уже отправлено")

    time_zone = users.get_user_data(message.chat.id)[5]
    if time_zone == "not_set":
        return await message.answer(Constants.settings_text["please_select_utc"]["ru"], parse_mode="HTML",
                                    reply_markup=keyboards.kb_main_menu)
    date = date_converter.utc(reminder[4], time_zone, mode='f')

    question = await message.answer(
        f"Дата: <b>{date_converter.get_day_of_the_week(date.split()[0])} {date}</b>\n"
        f"Id: <b>{reminder[3]}</b>\n"
        f"Текст: <b>{reminder[5]}</b>\n"
        f"Удалить напоминание?", parse_mode="HTML", reply_markup=keyboards.inline_kb_confirm)
    await state.update_data(message_id=question.message_id)


async def get_id_from_message(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Некорректный id!\nВведите id напоминания:")

    if not int(message.text) in [el[3] for el in reminders.get_user_reminders(message.chat.id)]:
        return await message.answer("Напоминания с id {reminder_id} не существует!\nВведите id напоминания:".format(
            reminder_id=int(message.text)), reply_markup=keyboards.kb_cancel)

    await state.update_data(reminder_id=int(message.text))
    await DeleteReminder.next()

    reminder = [el for el in reminders.get_user_reminders(message.chat.id) if el[3] == int(message.text)][0]
    time_zone = users.get_user_data(message.chat.id)[5]
    if time_zone == "not_set":
        return await message.answer(Constants.settings_text["please_select_utc"]["ru"], parse_mode="HTML",
                                    reply_markup=keyboards.kb_main_menu)
    date = date_converter.utc(reminder[4], time_zone, mode='f')

    question = await message.answer(
        f"Дата: <b>{date_converter.get_day_of_the_week(date.split()[0])} {date}</b>\n"
        f"Id: <b>{reminder[3]}</b>\n"
        f"Текст: <b>{reminder[5]}</b>\n"
        f"Удалить напоминание?", parse_mode="HTML", reply_markup=keyboards.inline_kb_confirm)
    await state.update_data(message_id=question.message_id)


async def get_id_from_call(call: types.CallbackQuery, state: FSMContext):
    if not int(call.data) in [el[3] for el in reminders.get_user_reminders(call.message.chat.id)]:
        return await call.message.answer("Напоминания с id {reminder_id} не существует!\nВведите id напоминания:".format(
            reminder_id=int(call.data)), reply_markup=keyboards.kb_cancel)

    await state.update_data(reminder_id=int(call.data))
    await DeleteReminder.next()

    reminder = [el for el in reminders.get_user_reminders(call.message.chat.id) if el[3] == int(call.data)][0]
    time_zone = users.get_user_data(call.message.chat.id)[5]
    if time_zone == "not_set":
        return await call.message.answer(Constants.settings_text["please_select_utc"]["ru"], parse_mode="HTML",
                                         reply_markup=keyboards.kb_main_menu)
    date = date_converter.utc(reminder[4], time_zone, mode='f')

    question = await call.message.answer(
        f"Дата: <b>{date_converter.get_day_of_the_week(date.split()[0])} {date}</b>\n"
        f"Id: <b>{reminder[3]}</b>\n"
        f"Текст: <b>{reminder[5]}</b>\n"
        f"Удалить напоминание?", parse_mode="HTML", reply_markup=keyboards.inline_kb_confirm)
    await state.update_data(message_id=question.message_id)


async def confirm_received(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    reminders.remove(id=data["reminder_id"], chat_id=call.message.chat.id)
    logger.debug("Deleted chat id {0} reminder with id: {1}".format(call.message.chat.id, data["reminder_id"]))

    user_data = users.get_user_data(call.message.chat.id)
    if user_data[3] == data["reminder_id"]:
        users.update_last_reminder(call.message.chat.id, 0)

    await call.bot.delete_message(call.message.chat.id, data["message_id"])
    await call.message.answer("Напоминание успешно удалено!", reply_markup=keyboards.kb_main_menu)
    await state.finish()


async def confirm_denied(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await call.bot.delete_message(call.message.chat.id, data["message_id"])
    await call.message.answer("Удаление напоминания отменено!", reply_markup=keyboards.kb_main_menu)
    await state.finish()


def register_handlers_delete(dp: Dispatcher):
    dp.register_message_handler(cmd_delete, commands="delete", state="*")
    dp.register_message_handler(cmd_delete, Text(equals=Constants.user_commands["delete"]["custom_name"]), state="*")
    dp.register_message_handler(cmd_undo, commands="undo", state="*")
    dp.register_message_handler(cmd_undo, Text(equals=Constants.user_commands["undo"]["custom_name"]), state="*")
    dp.register_message_handler(get_id_from_message, state=DeleteReminder.waiting_for_id)
    dp.register_callback_query_handler(get_id_from_call, text=Settings.ids_for_keyboard, state=DeleteReminder.waiting_for_id)
    dp.register_callback_query_handler(confirm_received, text="yes", state=DeleteReminder.waiting_for_confirm)
    dp.register_callback_query_handler(confirm_denied, text="no", state=DeleteReminder.waiting_for_confirm)
