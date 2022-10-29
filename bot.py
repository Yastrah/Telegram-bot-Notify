import logging
import threading
import asyncio
from datetime import datetime
# import emoji

from config.configuration import BotCommands

from app.data_scripts.config_reader import load_config
from app.handlers.message import register_handlers_message
from app.handlers.admin import register_handlers_admin
from app.handlers.common import register_handlers_common

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import BotCommand

from timetable import timer


version = "1.0.4"

logger = logging.getLogger(__name__)


async def set_commands(dispatcher: Dispatcher):
    """
    Регистрация команд, отображаемых в интерфейсе Telegram.
    """
    commands = [
        BotCommand(command=f"/{BotCommands.cmd_start}", description=BotCommands.cmd_start_description),
        BotCommand(command=f"/{BotCommands.cmd_help}", description=BotCommands.cmd_help_description),
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

    logger.info("""Product:
~~~Telegram-bot for quick reminders~~~
VERSION: {0}
LAST_UPDATE: {1}
The product is not commercial
Developed by Yastrah
GitHub: https://github.com/Yastrah""".format(version, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    register_handlers_common(dp)
    register_handlers_admin(dp)
    register_handlers_message(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == "__main__":
    from app.data_scripts import reminders_data  # временно, для тестирования
    reminders_data.reset()  # временно, для тестирования
    main()