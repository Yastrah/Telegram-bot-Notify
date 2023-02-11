import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config.config_reader import load_config
from bot.logic import date_converter
from bot.db import reminders
from bot import keyboards

logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


class DeleteReminder(StatesGroup):
    waiting_for_id = State()
    waiting_for_confirm = State()


async def cmd_delete(message: types.Message):
    data = reminders.get_user_reminders(message.chat.id)
    if not data:
        await message.answer("У вас нет напоминаний, чтобы их удалить")
        return

    await message.answer("Введите id напоминания:")
    await DeleteReminder.waiting_for_id.set()


async def id_received(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Некорректный id!\nВведите id напоминания:")
        return

    if not int(message.text) in [el[3] for el in reminders.get_user_reminders(message.chat.id)]:
        await message.answer("Напоминания с id {reminder_id} не существует!\nВведите id напоминания:".format(
            reminder_id=int(message.text)))
        return

    await state.update_data(reminder_id=message.text)
    await DeleteReminder.next()

    reminder = [el for el in reminders.get_user_reminders(message.chat.id) if el[3] == int(message.text)][0]

    await message.answer(f"Дата: <b>{date_converter.get_day_of_the_week(reminder[4].split()[0])} {reminder[4]}</b>\n"
                         f"Id: <b>{reminder[3]}</b>\n"
                         f"Текст: <b>{reminder[5]}</b>\n"
                         f"Удалить напоминание?", parse_mode="HTML", reply_markup=keyboards.inline_kb_confirm)


# @dp.callback_query_handler(text="yes")
async def confirm_received(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    reminders.remove(id=data["reminder_id"], chat_id=call.message.chat.id)
    logger.debug("Deleted chat id {0} reminder with id: {1}".format(call.message.chat.id, data["reminder_id"]))

    await call.message.answer("Напоминание успешно удалено!")
    await state.finish()


# @dp.callback_query_handler(text="no")
async def confirm_denied(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Удаление напоминания отменено!")
    await state.finish()



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


def register_handlers_delete(dp: Dispatcher):
    dp.register_message_handler(cmd_delete, commands="delete", state="*")
    dp.register_message_handler(id_received, state=DeleteReminder.waiting_for_id)
    dp.register_callback_query_handler(confirm_received, text="yes", state=DeleteReminder.waiting_for_confirm)
    dp.register_callback_query_handler(confirm_denied, text="no", state=DeleteReminder.waiting_for_confirm)
