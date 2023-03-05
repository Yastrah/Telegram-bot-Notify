import logging

from config.config_reader import load_config
from bot.db import reminders, users

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

    await message.answer(f"There are {len(users.read())} users in data base.\n"
                         f"Active reminders have {len(users_id)} users.")
    logger.debug("Admin {0} got users in database.".format(message.from_user.id))


async def cmd_send_all(message: types.Message):
    if str(message.from_user.id) not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    text = ' '.join(message.text.split()[1:])

    for user in users.read():
        await message.bot.send_message(chat_id=user[1], text=text)
    logger.debug("Admin {0} sent global message '{1}'.".format(message.from_user.id, text))


async def cmd_reset_data_base(message: types.Message):
    if str(message.from_user.id) not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    reminders_count = len(reminders.read())
    reminders.reset()
    logger.warning("Database was reset!")

    await message.answer(f"Database was reset. Deleted {reminders_count} reminders.")
    logger.debug("Admin {0} reset database.".format(message.from_user.id))


async def cmd_show_reports(message: types.Message):
    if str(message.from_user.id) not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    with open("data/reports.txt", mode='r', encoding="utf-8") as file:
        reports_count = int(file.readline())
        data = file.readlines()

    text = f"There are {reports_count} reports:\n\n"
    for row in data:
        text += f"{row.split(': ')[0]}:\n<b>{': '.join(row.split(': ')[1:])}</b>\n"

    await message.answer(text, parse_mode="HTML")
    logger.debug("Admin {0} got all reports.".format(message.from_user.id))


# async def cmd_archive_reports(message: types.Message):
#     if str(message.from_user.id) not in config.bot.admin_id:
#         logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
#         return



def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_users, commands="users", state="*")
    dp.register_message_handler(cmd_send_all, commands="send_all", state="*")
    dp.register_message_handler(cmd_reset_data_base, commands="reset_data", state="*")
    dp.register_message_handler(cmd_show_reports, commands="show_reports", state="*")
