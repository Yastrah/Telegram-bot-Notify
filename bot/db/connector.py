import sqlite3
import logging

from config.config_reader import load_config

logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


def on_start():
    """
    Проверка существования базы данных и таблиц, при необходимости их создание.
    :return: True. None - при вызове исключения.
    """

    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS reminders (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           chat_id VARCHAR NOT NULL,
                           message_id VARCHAR NOT NULL,
                           reminder_id INT32 NOT NULL,
                           date VARCHAR(19) NOT NULL,
                           content TEXT NOT NULL
                           )""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                           user_id VARCHAR PRIMARY KEY,
                           chat_id VARCHAR NOT NULL,
                           language VARCHAR NOT NULL,
                           last_reminder_id INT32 NOT NULL,
                           total_reminders INT64 NOT NULL,
                           using_since VARCHAR(10) NOT NULL
                           )""")

        return True

    except Exception as e:
        logger.error("Failed to create DataBase or tables!\n\tException: {0}".format(e))
        return None