import logging

from app.data_scripts.config_reader import load_config
from config.configuration import BotCommands

from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_start(message: types.Message):
    await message.answer(BotCommands.cmd_start_text["en"].format(config.bot.name), parse_mode="HTML")


async def cmd_help(message: types.Message):
    await message.answer(BotCommands.cmd_help_text["ru"].format(config.bot.name), parse_mode="HTML")


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=BotCommands.cmd_start, state="*")
    dp.register_message_handler(cmd_help, commands=BotCommands.cmd_help, state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
