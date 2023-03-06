import logging

from config.configuration import Settings
from config.config_reader import load_config

from bot.db import reminders, users

from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_users(message: types.Message):
    if message.from_user.id not in config.bot.admin_id:
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
    if message.from_user.id not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    text = ' '.join(message.text.split()[1:])

    for user in users.read():
        await message.bot.send_message(chat_id=user[1], text=text)
    logger.debug("Admin {0} sent global message '{1}'.".format(message.from_user.id, text))


async def cmd_reset_data_base(message: types.Message):
    if message.from_user.id not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    reminders_count = len(reminders.read())
    reminders.reset()
    logger.warning("Database was reset!")

    await message.answer(f"Database was reset. Deleted {reminders_count} reminders.")
    logger.warning("Admin {0} reset database.".format(message.from_user.id))


async def cmd_show_reports(message: types.Message):
    if message.from_user.id not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    with open("data/reports.txt", mode='r', encoding="utf-8") as file:
        reports_count = int(file.readline())
        data = file.readlines()

    if not data:
        return await message.answer("There are no reports.")

    text = f"There are {reports_count} reports:\n\n"
    for row in data:
        text += f"{row.split(': ')[0]}:\n<b>{': '.join(row.split(': ')[1:])}</b>\n"

    await message.answer(text, parse_mode="HTML")
    logger.debug("Admin {0} got all reports.".format(message.from_user.id))


async def cmd_archive_reports(message: types.Message):
    if message.from_user.id not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    with open("data/reports.txt", mode='r', encoding="utf-8") as file:
        reports_count = int(file.readline())
        data = file.read()

    if reports_count == 0:
        return await message.answer("There are no reports to archive!")

    with open("data/reports.txt", mode='w', encoding="utf-8") as file:
        file.write('0\n')

    with open("data/archived_reports.txt", mode='a', encoding="utf-8") as file:
        file.write(data)

    await message.answer(f"{reports_count} reports archived successfully.")
    logger.debug("Admin {0} archived {1} reports.".format(message.from_user.id, reports_count))


async def cmd_block_user(message: types.Message):
    if message.from_user.id not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    user_id = message.text.split()[1]
    Settings.blocked_users.append(int(user_id))

    with open("data/blocked_users.txt", mode='a', encoding="utf-8") as file:
        file.write(user_id + '\n')

    await message.answer(f"User {user_id} blocked.")
    logger.debug("Admin {0} blocked user {1}.".format(message.from_user.id, user_id))


async def cmd_unblock_user(message: types.Message):
    if message.from_user.id not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    user_id = message.text.split()[1]

    with open("data/blocked_users.txt", mode='r', encoding="utf-8") as file:
        blocked_users = file.read().split('\n')

    try:
        blocked_users.remove(user_id)
        Settings.blocked_users.remove(int(user_id))
    except:
        return await message.answer(f"User {user_id} is not blocked.")

    text = '\n'.join(blocked_users)

    with open("data/blocked_users.txt", mode='w', encoding="utf-8") as file:
        file.write(text)

    await message.answer(f"User {user_id} unblocked.")
    logger.debug("Admin {0} unblocked user {1}.".format(message.from_user.id, user_id))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_users, commands="users", state="*")
    dp.register_message_handler(cmd_send_all, commands="send_all", state="*")
    dp.register_message_handler(cmd_reset_data_base, commands="reset_data", state="*")
    dp.register_message_handler(cmd_show_reports, commands="show_reports", state="*")
    dp.register_message_handler(cmd_archive_reports, commands="archive_reports", state="*")
    dp.register_message_handler(cmd_block_user, commands="block_user", state="*")
    dp.register_message_handler(cmd_unblock_user, commands="unblock_user", state="*")
