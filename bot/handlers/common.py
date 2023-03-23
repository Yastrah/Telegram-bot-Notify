import logging
import datetime

from config.config_reader import load_config
from config.configuration import Constants, Settings
from bot.handlers.settings import register_user

from bot import keyboards
from bot.db import users


from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_start(message: types.Message, state: FSMContext):
    if not users.get_user_data(str(message.chat.id)):
        return await register_user(message, state)

    start = Constants.user_commands.get("start")
    await message.answer(start["text"]["ru"].format(bot_name=config.bot.name), parse_mode="HTML",
                         reply_markup=keyboards.kb_main_menu)



async def cmd_help(message: types.Message):
    help = Constants.user_commands.get("help")
    await message.answer(help["text"]["ru"].format(bot_name=config.bot.name), parse_mode="HTML",
                         reply_markup=keyboards.kb_main_menu)


async def cmd_menu(message: types.Message, state: FSMContext):
    await message.answer("Вы вернулись в главное меню", reply_markup=keyboards.kb_main_menu)
    await state.finish()


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")
    dp.register_message_handler(cmd_menu, commands="menu", state="*")
    dp.register_message_handler(cmd_menu, Text(equals=Constants.user_commands["menu"]["custom_name"]), state="*")
