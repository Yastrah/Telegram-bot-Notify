import logging

from config.config_reader import load_config
from bot.logic import date_converter
from bot.db import reminders

from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_reminders_list(message: types.Message):
    data = reminders.get_user_reminders(message.chat.id)

    if data:
        data.sort(key=lambda x: x[3])
        reminders_list = "<b>🔻Список активных напоминаний🔻</b>\n\n"  # ➖ ️〰️

        for row in data:
            reminders_list += f"Дата: <b>{date_converter.get_day_of_the_week(row[4].split()[0])} {row[4]}</b>\n" \
                              f"Id: <b>{row[3]}</b>\n" \
                              f"Текст: <b>{row[5]}</b>\n\n"

        # logger.debug("Created reminder:\t chat_id: {0}, "
        #              "reminder_id: {1}, time: {2}, text: {3}".format(message.chat.id, reminder_id, full_date, text))
        await message.answer(reminders_list, parse_mode="HTML")
    else:
        await message.answer("У вас нет активных напоминаний.")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_reminders_list, commands="list", state="*")
    # dp.register_message_handler(cmd_help, commands="help", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
