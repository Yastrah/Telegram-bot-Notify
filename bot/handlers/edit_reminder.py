import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from config.config_reader import load_config
from config.configuration import Constants
from bot.logic import date_converter
from bot.db import reminders, users
from bot import keyboards


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


class EditReminder(StatesGroup):
    waiting_for_id = State()
    waiting_for_edit_type = State()
    waiting_for_confirm = State()


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

    await state.update_data(reminder_id=message.text)
    await EditReminder.next()

    reminder = [el for el in reminders.get_user_reminders(message.chat.id) if el[3] == int(message.text)][0]

    await message.answer(f"Дата: <b>{date_converter.get_day_of_the_week(reminder[4].split()[0])} {reminder[4]}</b>\n"
                         f"Id: <b>{reminder[3]}</b>\n"
                         f"Текст: <b>{reminder[5]}</b>\n"
                         f"Что вы хотите изменить?", parse_mode="HTML", reply_markup=keyboards.inline_kb_edit_type)


def register_handlers_edit(dp: Dispatcher):
    dp.register_message_handler(cmd_edit, commands="edit", state="*")
    dp.register_message_handler(cmd_edit, Text(equals=Constants.user_commands["edit"]["custom_name"]), state="*")
    dp.register_message_handler(id_received, state=EditReminder.waiting_for_id)
    # dp.register_callback_query_handler(confirm_received, text="yes", state=DeleteReminder.waiting_for_confirm)
    # dp.register_callback_query_handler(confirm_denied, text="no", state=DeleteReminder.waiting_for_confirm)


# class EditReminder(StatesGroup):
#     waiting_for_team_name = State()
#     waiting_for_character_name = State()
#     waiting_for_character_class = State()
#     waiting_for_character_stats = State()
#
#
# async def team_start(message: types.Message):
#     verification = protect.user_already_has_team(message.from_user.id)
#     if verification is not True:
#         logger.debug(f"User: {message.from_user.id}. Team is already exist!")
#         await message.answer(verification)
#         return
#
#     await message.answer("Введите имя команды:")
#     await EditReminder.waiting_for_team_name.set()
#
#
# async def team_name_chosen(message: types.Message, state: FSMContext):
#     verification = protect.team_name(message.text)
#     if verification is not True:
#         logger.debug(f"User: {message.from_user.id}. Invalid characters name!")
#         await message.answer(f"{verification}\nВведите имя команды ещё раз:")
#         return
#
#     await state.update_data(team_name=message.text)
#
#     # Для последовательных шагов можно не указывать название состояния, обходясь next()
#     await EditReminder.next()
#     await message.answer("Теперь выберите имя первого члена команды:")
#
#
# async def team_character_name_chosen(message: types.Message, state: FSMContext):
#     # await state.update_data(team_character_name=message.text)
#
#     # получение рандомного персонажа
#
#     user_data = await state.get_data()
#
#     db.add_team(message.from_user.id, user_data["team_name"], [{"name": message.text, "stats": "None"}])
#
#     await message.answer(f"""Вы создали команду "{user_data["team_name"]}".\n"""
#                          f"Первого члена команды зовут {message.text}.")
#     await state.finish()
#
#
# def register_handlers_team(dp: Dispatcher):
#     dp.register_message_handler(team_start, commands=config.bot_commands.new_team, state="*")
#     dp.register_message_handler(team_name_chosen, state=EditReminder.waiting_for_team_name)
#     dp.register_message_handler(team_character_name_chosen, state=EditReminder.waiting_for_character_name)