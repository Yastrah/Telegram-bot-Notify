import logging
import datetime

from config.config_reader import load_config
from config.configuration import Constants, Settings

from bot import keyboards
from bot.db import users


from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def register_user(message: types.Message, state: FSMContext):
    now_date = datetime.datetime.now().strftime(Settings.date_format).split()[0]
    # Добавить выбор языка
    uts_select = await message.answer(Constants.settings_text["selecting_utc"]["ru"], parse_mode="HTML", reply_markup=keyboards.inline_kb_utc)
    await state.update_data(message_id=uts_select.message_id)

    users.add_user(str(message.from_user.id), str(message.chat.id), 'ru', 0, "not_set", now_date)
    logger.warning("Registered new user. user_id: {0}, chat_id: {1}, user_name: {2}".format(message.from_user.id,
                                                                                            message.chat.id,
                                                                                            message.from_user.username))


async def cmd_settings(message: types.Message, state: FSMContext):
    data = users.get_user_data(message.chat.id)
    if data[5] == "not_set":
        uts_select = await message.answer(Constants.settings_text["selecting_utc"]["ru"], parse_mode="HTML",
                                          reply_markup=keyboards.inline_kb_utc)
        return await state.update_data(message_id=uts_select.message_id)

    settings = Constants.user_commands.get("settings")
    await message.answer(settings["text"]["ru"].format(registered=data[6], reminders_sent=data[4], language="🇷🇺 русский", time_zone=data[5]),
                         parse_mode="HTML", reply_markup=keyboards.inline_kb_edit_settings)


async def set_utc(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.bot.delete_message(call.message.chat.id, data["message_id"])

    time_zone = call.data.split()[1]

    users.update_time_zone(call.message.chat.id, time_zone)
    logger.debug("User {0} set time_zone {1}.".format(call.message.chat.id, time_zone))
    await call.message.answer(Constants.settings_text["utc_set"]["ru"].format(time_zone=time_zone),
                              parse_mode="HTML", reply_markup=keyboards.kb_main_menu)


async def confirm_received(call: types.CallbackQuery, state: FSMContext):
    pass


def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(cmd_settings, commands="settings", state="*")
    dp.register_callback_query_handler(set_utc, text=Settings.callback_utc_data, state='*')
