import logging
import re

from app.config_reader import load_config
from app import dataBase

from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def create_notification(message: types.Message):
    time_pattern = re.compile("\d{1,2}([:. /])\d{1,2}")

    time = time_pattern.search(message)


    # dataBase.add_new()
    await message.answer("Уведомление успешно создано.")


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(create_notification, content_types=types.Message, state="*")
    # dp.register_message_handler(cmd_help, commands="help", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")