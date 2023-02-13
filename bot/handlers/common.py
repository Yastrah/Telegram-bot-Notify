import logging

from config.config_reader import load_config
from config.configuration import Constants

from bot import keyboards

from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def cmd_start(message: types.Message):
    start = Constants.user_commands.get("start")
    await message.answer(start["text"]["ru"].format(bot_name=config.bot.name), parse_mode="HTML",
                         reply_markup=keyboards.kb_main_menu)


async def cmd_help(message: types.Message):
    help = Constants.user_commands.get("help")
    await message.answer(help["text"]["ru"].format(bot_name=config.bot.name), parse_mode="HTML",
                         reply_markup=keyboards.kb_main_menu)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await message.answer("Состояние сброшено", reply_markup=keyboards.kb_main_menu)
    await state.finish()


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals=Constants.user_commands["cancel"]["custom_name"]),
                                state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
