import logging
import threading
import asyncio
from datetime import datetime
# import emoji

from config.configuration import Constants

from config.config_reader import load_config
from bot.handlers.messages import register_handlers_messages
from bot.handlers.admin import register_handlers_admin
from bot.handlers.common import register_handlers_common
from bot.handlers.errors import register_handlers_error
from bot.handlers.client import register_handlers_client

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import BotCommand

from bot.send_reminders import timer


version = "1.0.6"

logger = logging.getLogger(__name__)


async def set_commands(dispatcher: Dispatcher):
    """
    Регистрация команд, отображаемых в интерфейсе Telegram.
    """
    commands = [BotCommand(command=f"/{command}", description=data.get("description"))
                for command, data in Constants.user_commands.items()]

    await dispatcher.bot.set_my_commands(commands)
    logger.info("Bot commands have been set.")

def register_all_handlers(dp: Dispatcher):
    register_handlers_admin(dp)
    register_handlers_common(dp)
    register_handlers_client(dp)
    register_handlers_messages(dp)
    register_handlers_error(dp)


async def on_startup(dispatcher):
    await set_commands(dispatcher)

    loop = asyncio.get_event_loop()

    th = threading.Thread(target=timer, args=[dispatcher.bot, loop])
    th.start()

    logger.info("Start schedule process.")


async def on_shutdown(dispatcher):
    # Проверка бд и т.п.
    logger.warning("Shutdown dispatcher!!!")


def main():
    config = load_config("config/bot.ini")

    logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=config.logger.level,
                        datefmt="%Y-%m-%d %H:%M:%S")

    bot = Bot(token=config.bot.token)
    dp = Dispatcher(bot)

    logger.info("""Product:
~~~Telegram-bot for quick reminders~~~
VERSION: {0}
LAST_UPDATE: {1}
The product is not commercial
Developed by Yastrah
GitHub: https://github.com/Yastrah""".format(version, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    register_all_handlers(dp)

    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
    except Exception as e:
        logger.error("Could not start polling!\n\tException: {0}".format(e))

if __name__ == "__main__":
    # from bot.db import reminders  # временно, для тестирования
    # reminders.reset()  # временно, для тестирования
    main()
