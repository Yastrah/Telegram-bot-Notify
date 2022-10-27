import logging
import threading
import asyncio
# import emoji

from app.data_scripts.config_reader import load_config
from app.handlers.message import register_handlers_message
from app.handlers.admin import register_handlers_admin
from app.handlers.common import register_handlers_common

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import BotCommand

from timetable import timer


version = "1.0.3"

logger = logging.getLogger(__name__)


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(dispatcher: Dispatcher):
    commands = [
        BotCommand(command=f"/start", description="начать"),
        BotCommand(command=f"/help", description="помощь в использовании"),
        BotCommand(command=f"/today", description="список дел на сегодня"),
    ]
    await dispatcher.bot.set_my_commands(commands)

    logger.info("Bot commands have been set.")


async def on_startup(dispatcher):
    await set_commands(dispatcher)

    loop = asyncio.get_event_loop()

    th = threading.Thread(target=timer, args=[dispatcher.bot, loop])
    th.start()

    logger.info("Start schedule process.")


def main():
    config = load_config("config/bot.ini")

    logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=config.logger.level,
                        datefmt="%Y-%m-%d %H:%M:%S")

    bot = Bot(token=config.bot.token)
    dp = Dispatcher(bot)

    logger.info(f"VERSION: {version}")

    register_handlers_common(dp)
    register_handlers_admin(dp)
    register_handlers_message(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == "__main__":
    from app.data_scripts import reminders_data  # временно, для тестирования
    reminders_data.reset()  # временно, для тестирования
    main()