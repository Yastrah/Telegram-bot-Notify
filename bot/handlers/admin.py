import logging

from config.config_reader import load_config
from bot.db import reminders

from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_users(message: types.Message):
    if str(message.from_user.id) not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    users_id = []
    for reminder in reminders.read():
        if not reminder[1] in users_id:
            users_id.append(reminder[1])

    await message.answer(f"There are {len(users_id)} users in data base.")
    logger.debug("Admin {0} got users in data base.".format(message.from_user.id))


async def cmd_send_all(message: types.Message):
    if str(message.from_user.id) not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    text = ' '.join(message.text.split()[1:])

    chats_id = []
    for reminder in reminders.read():
        if not reminder[1] in chats_id:
            chats_id.append(reminder[1])

    for chat_id in chats_id:
        await message.bot.send_message(chat_id=chat_id, text=text)
    logger.debug("Admin {0} sent global message '{1}'.".format(message.from_user.id, text))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_users, commands="users", state="*")
    dp.register_message_handler(cmd_send_all, commands="send_all", state="*")
