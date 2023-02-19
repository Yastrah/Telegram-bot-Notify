import sqlite3
import logging

from config.config_reader import load_config

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
    Получение данных о конкретном пользователе (user_id, chat_id, language, last_reminder_id, total_reminders, using_since).
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


def update_last_reminder(user_id: str, last_reminder_id: int) -> bool:
    """
    Изменяет id последнего напоминания для пользователя
    :param user_id: id пользователя
    :param last_reminder_id: новое idдля последнего напоминания
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE users SET last_reminder_id=? WHERE user_id=?""", [last_reminder_id, user_id])

        return True

    except Exception as e:
        logger.error("Failed to update user_id {0} last_reminder_id {1}!\n\tException: {2}".format(user_id, last_reminder_id, e))
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
        logger.error("Failed to update user_id {0} last_reminder_id {1}!\n\tException: {2}".format(user_id, last_reminder_id, e))
        return None


def add_user(user_id: str, chat_id: str, language: str, last_reminder_id: int, using_since: str) -> bool:
    """
    Добавляет пользователя в базу данных.
    :param user_id:
    :param chat_id:
    :param language:
    :param last_reminder_id:
    :param using_since:
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("""INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)""",
                           [user_id, chat_id, language, last_reminder_id, 0, using_since])

        return True

    except Exception as e:
        logger.error("Failed to add user_id {0} to database!\n\tException: {1}".format(user_id, e))
        return None
