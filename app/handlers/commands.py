import logging
from app.config_reader import load_config
from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_start(message: types.Message):
    await message.reply(f"Hi!\nI'm <u><b>{config.bot.name}</b>!</u>\nDesigned by Yastrah.", parse_mode="HTML")


async def cmd_help(message: types.Message):
    await message.answer(f"{config.bot.name} - это бот позволяющий создать напоминания.\nКомады:\n...")


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
