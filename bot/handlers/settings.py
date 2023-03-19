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


async def cmd_settings(message: types.Message):
    settings = Constants.user_commands.get("settings")
    await message.answer(settings["text"]["ru"], parse_mode="HTML",
                         reply_markup=keyboards.kb_main_menu)


async def set_utc(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.bot.delete_message(call.message.chat.id, data["message_id"])

    delta_time = call.data.split()[1]

    users.update_time_zone(call.message.chat.id, delta_time)
    logger.debug("User {0} set time_zone {1}.".format(call.message.chat.id, delta_time))


def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(cmd_settings, commands="settings", state="*")
    dp.register_callback_query_handler(set_utc, text='utc -11:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc -10:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc -09:30', state='*')
    dp.register_callback_query_handler(set_utc, text='utc -09:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc -08:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc -07:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc -06:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc -05:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc -04:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc -03:30', state='*')
    dp.register_callback_query_handler(set_utc, text='utc -03:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc -02:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc -01:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc ±00:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +01:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +02:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +03:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +03:30', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +04:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +04:30', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +05:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +05:30', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +05:45', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +06:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +06:30', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +07:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +08:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +08:45', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +09:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +09:30', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +10:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +10:30', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +11:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +12:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +13:00', state='*')
    dp.register_callback_query_handler(set_utc, text='utc +14:00', state='*')
