import logging

from bot.handlers.settings import register_user
from config.config_reader import load_config
from config.configuration import Constants, Settings
from bot.logic import date_converter
from bot.db import reminders, users
from bot import keyboards

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_reminders_list(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in Settings.blocked_users:
        return await message.answer("🔒 К сожалению вы заблокированны!")

    if not users.get_user_data(str(message.chat.id)):
        return await register_user(message, state)

    time_zone = users.get_user_data(message.chat.id)[5]
    if time_zone == "not_set":
        return await message.answer(Constants.settings_text["please_select_utc"]["ru"], parse_mode="HTML",
                                    reply_markup=keyboards.kb_main_menu)
    reminders_data = reminders.get_user_reminders(message.chat.id)

    if not reminders_data:
        return await message.answer("⚡️ У вас нет активных напоминаний.", reply_markup=keyboards.kb_main_menu)

    reminders_data.sort(key=lambda x: ''.join(list(reversed(x[4].split()[0].split('/'))) + x[4].split()[1].split(':')))
    data = {}
    for row in reminders_data:
        date = date_converter.utc(row[4], time_zone, mode='f').split()
        if data.get(row[4].split()[0]):
            data[date[0]].append({"time": date[1], "id": row[3], "text": row[5]})
        else:
            data[date[0]] = [{"time": date[1], "id": row[3], "text": row[5]}]

    reminders_list_message = Constants.reminders_format["list_title"]["ru"]

    for date, reminders_list in data.items():

        reminders_list_message += Constants.reminders_format["day_title"]["ru"].format(
            day_of_the_week=date_converter.get_day_of_the_week(date),
            date=date
        )

        for reminder in reminders_list:
            reminders_list_message += Constants.reminders_format["reminder_in_list"]["ru"].format(
                time=reminder['time'],
                id=reminder['id'],
                text=reminder['text']
            )

    await message.answer(reminders_list_message, parse_mode="HTML", reply_markup=keyboards.kb_main_menu)



def register_handlers_list(dp: Dispatcher):
    dp.register_message_handler(cmd_reminders_list, commands="list", state="*")
    dp.register_message_handler(cmd_reminders_list, Text(equals=Constants.user_commands["list"]["custom_name"]), state="*")
