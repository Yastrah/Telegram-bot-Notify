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


async def register_user(message: types.Message):
    now_date = datetime.datetime.now().strftime(Settings.date_format).split()[0]
    # Добавить выбор языка
    users.add_user(str(message.from_user.id), str(message.chat.id), 'ru', 0, now_date)
    logger.warning("Registered new user. user_id: {0}, chat_id: {1}, user_name: {2}".format(message.from_user.id,
                                                                                            message.chat.id,
                                                                                            message.from_user.username))


async def cmd_start(message: types.Message):
    start = Constants.user_commands.get("start")
    await message.answer(start["text"]["ru"].format(bot_name=config.bot.name), parse_mode="HTML",
                         reply_markup=keyboards.kb_main_menu)

    if not users.get_user_data(str(message.chat.id)):
        await register_user(message)


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
