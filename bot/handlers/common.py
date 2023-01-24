import logging

from bot.db.config_reader import load_config
from config.configuration import User

from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_start(message: types.Message):
    start = User.user_commands.get("start")
    await message.answer(start["text"]["en"].format(config.bot.name), parse_mode="HTML")


async def cmd_help(message: types.Message):
    help = User.user_commands.get("help")
    await message.answer(help["text"]["ru"].format(config.bot.name), parse_mode="HTML")


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
