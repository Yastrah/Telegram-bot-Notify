import sqlite3
import logging

from app.data_scripts.config_reader import load_config
from app.data_scripts.bot_data_base_connector import on_start

logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


def read() -> list:
    """
    Получение данных из DataBase.\n
    :return: Данные в виде списка кортежей (id, chat_id, message_id, date, content). None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM reminders")

        return cursor.fetchall()

    except Exception as e:
        logger.error("Failed to read DataBase!\n\tException: {0}".format(e))
        return None


def get_now(time) -> list:
    """
    Получение данных из DataBase с заданной датой и временем.\n
    :return: Данные в виде списка кортежей (id, chat_id, message_id, date, content). None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM reminders WHERE date=?", [time])

        return cursor.fetchall()

    except Exception as e:
        logger.error("Failed to read DataBase!\n\tException: {0}".format(e))
        return None


def add_new(chat_id: str, message_id: str, time: str, text: str):
    """
    Добавление нового напоминания в DataBase.\n
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("""INSERT INTO reminders(chat_id, message_id, date, content)
            VALUES (?, ?, ?, ?)""", [chat_id, message_id, time, text])

        return True

    except Exception as e:
        logger.error("Failed to add reminder to DataBase!\n\tException: {0}".format(e))
        return None


def remove(id=None, chat_id=None):
    """
    Удаляет уведомление с заданным id или удаляет все уведомления определённого пользователя.\n
    :param id: уведомления, которое необходимо удалить
    :param chat_id: пользователя, все уведомления кторого необходимо удалить
    :return:
    """
    if id:
        try:
            with sqlite3.connect(config.data.bot_db) as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM reminders WHERE id=?", [id])

            return True

        except Exception as e:
            logger.error("Failed to remove reminder from DataBase!\n\tException: {0}".format(e))
            return None

    elif chat_id:
        try:
            with sqlite3.connect(config.data.bot_db) as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM reminders WHERE chat_id=?", [chat_id])

            return True

        except Exception as e:
            logger.error("Failed to remove reminders from DataBase!\n\tException: {0}".format(e))
            return None

    else:
        return None


def reset():
    """
    Полностью удаляет все данные из db.\n
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("DROP TABLE IF EXISTS reminders")
            on_start()

        return True

    except Exception as e:
        logger.error("Failed to reset database!\n\tException: {0}".format(e))
        return None
