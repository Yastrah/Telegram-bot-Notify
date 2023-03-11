import logging

from config.configuration import Settings
from config.config_reader import load_config

from bot.db import reminders, users

from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_show_users(message: types.Message):
    if message.from_user.id not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    users_info = []
    for user in users.read():
        info = await message.bot.get_chat_member(user[0], user[1])
        users_info.append(f"{user[0]}; {user[1]}; {info['user']['first_name']}; @{info['user']['username']}")

    text = '\n'.join(users_info)

    await message.answer(f"There are <b>{len(users.read())}</b> users in database.\n"
                         f"Active reminders have <b>{len(users_info)}</b> users.\n\n"
                         f"user_id; chat_id; firstname; username:\n<b>{text}</b>", parse_mode="HTML")
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

    await message.answer(f"Database was reset. Deleted <b>{reminders_count}</b> reminders.", parse_mode="HTML")
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


async def cmd_show_blocked_users(message: types.Message):
    if message.from_user.id not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    text = '\n'.join(Settings.blocked_users)
    await message.answer(f"Blocked users:\n<b>{text}</b>", parse_mode="HTML")
    logger.debug("Admin {0} got the list of blocked users.".format(message.from_user.id))


async def cmd_block_user(message: types.Message):
    if message.from_user.id not in config.bot.admin_id:
        logger.debug("Admin access denied for user {0}!".format(message.from_user.id))
        return

    user_id = message.text.split()[1]

    if int(user_id) in Settings.blocked_users:
        return await message.answer(f"User <b>{user_id}</b> is already blocked.", parse_mode="HTML")

    Settings.blocked_users.append(int(user_id))

    with open("data/blocked_users.txt", mode='a', encoding="utf-8") as file:
        file.write(user_id + '\n')

    await message.answer(f"User <b>{user_id}</b> blocked.", parse_mode="HTML")
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
        return await message.answer(f"User <b>{user_id}</b> is not blocked.", parse_mode="HTML")

    text = '\n'.join(blocked_users)

    with open("data/blocked_users.txt", mode='w', encoding="utf-8") as file:
        file.write(text)

    await message.answer(f"User <b>{user_id}</b> unblocked.", parse_mode="HTML")
    logger.debug("Admin {0} unblocked user {1}.".format(message.from_user.id, user_id))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_show_users, commands="show_users", state="*")
    dp.register_message_handler(cmd_send_all, commands="send_all", state="*")
    dp.register_message_handler(cmd_reset_data_base, commands="reset_data", state="*")
    dp.register_message_handler(cmd_show_reports, commands="show_reports", state="*")
    dp.register_message_handler(cmd_archive_reports, commands="archive_reports", state="*")
    dp.register_message_handler(cmd_show_blocked_users, commands="show_blocked_users", state="*")
    dp.register_message_handler(cmd_block_user, commands="block_user", state="*")
    dp.register_message_handler(cmd_unblock_user, commands="unblock_user", state="*")
