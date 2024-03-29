import sqlite3
import logging

from config.config_reader import load_config
from bot.db.connector import on_start


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


def read() -> list:
    """
    Получение данных из DataBase.
    :return: Данные в виде списка кортежей (user_id, chat_id, language, last_reminder_id, total_reminders, using_since).
    None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users")

        return cursor.fetchall()

    except Exception as e:
        logger.error("Failed to read table users!\n\tException: {0}".format(e))
        return None


def get_user_data(chat_id: str) -> tuple:
    """
    Получение данных о конкретном пользователе (user_id, chat_id, language, last_reminder_id, total_reminders,
    time_zone, using_since).\n
    :param chat_id: чат id пользователя
    :return:
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE chat_id=?", [chat_id])

        return cursor.fetchone()

    except Exception as e:
        logger.error("Failed to get chat_id {0} data!\n\tException: {1}".format(chat_id, e))
        return None


def update_last_reminder(chat_id: str, last_reminder_id: int) -> bool:
    """
    Изменяет id последнего напоминания для пользователя
    :param chat_id: чат id пользователя
    :param last_reminder_id: новое idдля последнего напоминания
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE users SET last_reminder_id=? WHERE chat_id=?""", [last_reminder_id, chat_id])

        return True

    except Exception as e:
        logger.error("Failed to update chat_id {0} last_reminder_id {1}!\n\tException: {2}".format(chat_id, last_reminder_id, e))
        return None


def update_total_reminders(chat_id: str) -> bool:
    """
    На одно увеличивает количество полученных пользователем напоминаний.
    :param chat_id: чат id пользователя
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("SELECT total_reminders FROM users WHERE chat_id=?", [chat_id])
            total_reminders = cursor.fetchone()[0]

            cursor.execute("""UPDATE users SET total_reminders=? WHERE chat_id=?""", [total_reminders+1, chat_id])

        return True

    except Exception as e:
        logger.error("Failed to update chat_id {0} total_reminders!\n\tException: {1}".format(chat_id, e))
        return None


def update_time_zone(chat_id: str, time_zone: int) -> bool:
    """
    На одно увеличивает количество полученных пользователем напоминаний.
    :param chat_id: чат id пользователя
    :param time_zone: новое значение UTS
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE users SET time_zone=? WHERE chat_id=?""", [time_zone, chat_id])

        return True

    except Exception as e:
        logger.error("Failed to update chat_id {0} time_zone!\n\tException: {1}".format(chat_id, e))
        return None


def add_user(user_id: str, chat_id: str, language: str, last_reminder_id: int, time_zone: int, using_since: str) -> bool:
    """
    Добавляет пользователя в базу данных.
    :param user_id:
    :param chat_id:
    :param language:
    :param last_reminder_id:
    :param time_zone:
    :param using_since:
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("""INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)""",
                           [user_id, chat_id, language, last_reminder_id, 0, time_zone, using_since])

        return True

    except Exception as e:
        logger.error("Failed to add user_id {0} to database!\n\tException: {1}".format(user_id, e))
        return None


def remove_user(user_id: str):
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM users WHERE user_id=?", [user_id])

        return True

    except Exception as e:
        logger.error("Failed to remove user {0} from table users!\n\tException: {1}".format(user_id, e))
        return None


def reset():
    """
    Полностью удаляет все данные из db.
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("DROP TABLE IF EXISTS users")
            on_start()

        return True

    except Exception as e:
        logger.error("Failed to reset database!\n\tException: {0}".format(e))
        return None
