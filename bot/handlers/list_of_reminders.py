import logging

from config.config_reader import load_config
from config.configuration import Constants, Settings
from bot.logic import date_converter
from bot.db import reminders
from bot import keyboards

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_reminders_list(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in Settings.blocked_users:
        return await message.answer("🔒 К сожалению вы заблокированны!")

    data = reminders.get_user_reminders(message.chat.id)

    if data:
        data.sort(key=lambda x: x[3])
        reminders_list = "<b>🔻Список активных напоминаний🔻</b>\n\n"  # ➖ 〰️ 🔻

        for row in data:
            reminders_list += f"Дата: <b>{date_converter.get_day_of_the_week(row[4].split()[0])} {row[4]}</b>\n" \
                              f"Id: <b>{row[3]}</b>\n" \
                              f"Текст: <b>{row[5]}</b>\n\n"

        await message.answer(reminders_list, parse_mode="HTML", reply_markup=keyboards.kb_main_menu)
    else:
        await message.answer("⚡️ У вас нет активных напоминаний.", reply_markup=keyboards.kb_main_menu)


def register_handlers_list(dp: Dispatcher):
    dp.register_message_handler(cmd_reminders_list, commands="list", state="*")
    dp.register_message_handler(cmd_reminders_list, Text(equals=Constants.user_commands["list"]["custom_name"]), state="*")
