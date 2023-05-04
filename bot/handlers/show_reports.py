import logging
import re

from config.config_reader import load_config
from config.configuration import Settings, Constants

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_my_reports(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in Settings.blocked_users:
        return await message.answer("🔒 К сожалению вы заблокированны!")

    with open("data/reports.txt", mode='r', encoding="utf-8") as file:
        file.readline()
        file.readline()
        data = file.read()

    if data:
        pattern = re.compile(fr"{message.from_user.id}.+\n")
        match = pattern.findall(data)

        text = Constants.user_commands["my_reports"]["list_title"]['ru']
        for rep in match:
            text += rep + '\n'

        return await message.answer(text, parse_mode="HTML")

    else:
        return await message.answer(Constants.user_commands["my_reports"]["no_reports"]['ru'], parse_mode="HTML")


def register_handlers_my_reports(dp: Dispatcher):
    dp.register_message_handler(cmd_my_reports, commands="my_reports", state="*")
