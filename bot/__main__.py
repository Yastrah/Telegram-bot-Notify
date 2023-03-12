import logging
import threading
import asyncio
from datetime import datetime
import sys

from config.configuration import Constants
from config.config_reader import load_config

from bot.send_reminders import timer
from bot.handlers.admin import register_handlers_admin
from bot.handlers.common import register_handlers_common
from bot.handlers.delete_reminder import register_handlers_delete
from bot.handlers.list_of_reminders import register_handlers_list
from bot.handlers.edit_reminder import register_handlers_edit
from bot.handlers.report import register_handlers_report
from bot.handlers.messages import register_handlers_messages
from bot.handlers.errors import register_handlers_error

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import BotCommand


version = "1.2.8"

logger = logging.getLogger(__name__)


def register_all_handlers(dp: Dispatcher):
    """
    Регистрация всех обработчиков сообщений и команд.
    """
    register_handlers_admin(dp)
    register_handlers_common(dp)
    register_handlers_list(dp)
    register_handlers_delete(dp)
    register_handlers_edit(dp)
    register_handlers_report(dp)
    register_handlers_messages(dp)
    register_handlers_error(dp)


async def set_commands(dispatcher: Dispatcher):
    """
    Регистрация команд, отображаемых в интерфейсе Telegram.
    """
    commands = [BotCommand(command=f"{command}", description=data.get("description"))
                for command, data in Constants.user_commands.items()]

    await dispatcher.bot.set_my_commands(commands)
    logger.info("Bot commands have been set.")


async def on_startup(dispatcher):
    """
    Запуск параллельного потока с таймером при запуске диспетчера.
    """
    await set_commands(dispatcher)

    loop = asyncio.get_event_loop()

    th = threading.Thread(target=timer, args=[dispatcher.bot, loop])
    th.start()

    logger.info("Start schedule process.")


async def on_shutdown(dispatcher):
    logger.warning("Shutdown dispatcher!!!")
    pass

def main():
    file_log = logging.FileHandler(filename=f"logs/bot_logs_{datetime.now().strftime('%Y_%m_%d')}.log", encoding="utf-8")
    file_log.setLevel("DEBUG")

    console_log = logging.StreamHandler(stream=sys.stderr)
    console_log.setLevel("INFO")

    logging.getLogger("aiogram").setLevel("INFO")
    logging.getLogger("asyncio").setLevel("INFO")
    logging.getLogger("schedule").setLevel("INFO")
    logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level="DEBUG",
                        datefmt="%Y-%m-%d %H:%M:%S", handlers=[file_log, console_log])

    config = load_config("config/bot.ini")

    bot = Bot(token=config.bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

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
    main()
    # from bot.db import protection
    # protection.checking_for_old_reminders()