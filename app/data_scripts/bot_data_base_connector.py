import sqlite3
import logging

from app.data_scripts.config_reader import load_config

logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


def on_start():
    """
    Проверка существования базы данных и таблиц, при необходимости их создание.\n
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS reminders (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           chat_id VARCHAR NOT NULL,
                           message_id VARCHAR NOT NULL,
                           date VARCHAR(19) NOT NULL,
                           content TEXT NOT NULL
                           )""")

            # Создание таблицы users
            # cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            #                id INTEGER PRIMARY KEY AUTOINCREMENT,
            #                chat_id VARCHAR NOT NULL,
            #                message_id VARCHAR NOT NULL,
            #                date VARCHAR(19) NOT NULL,
            #                content TEXT NOT NULL
            #                )""")

        return True

    except Exception as e:
        logger.error("Failed to create DataBase or tables!\n\tException: {0}".format(e))
        return None