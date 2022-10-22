import logging

from app.config_reader import load_config
from app import data_base

from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_users(message: types.Message):
    logger.debug("Admin command request.")

    if str(message.from_user.id) != config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    await message.answer(f"Сейчас в базе данных {len(data_base.read().keys())} пользователей.")



def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_users, commands="users", state="*")