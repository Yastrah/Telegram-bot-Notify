import sqlite3
import logging

from config.config_reader import load_config
from bot.db.connector import on_start

logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


def read() -> list:
    """
    Получение данных из DataBase.
    :return: Данные в виде списка кортежей (id, chat_id, message_id, reminder_id, date, content). None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM reminders")

        return cursor.fetchall()

    except Exception as e:
        logger.error("Failed to read table reminders!\n\tException: {0}".format(e))
        return None


def get_now(time) -> list:
    """
    Получение данных из DataBase с заданной датой и временем.
    :return: Данные в виде списка кортежей (id, chat_id, message_id, reminder_id, date, content). None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM reminders WHERE date=?", [time])

        return cursor.fetchall()

    except Exception as e:
        logger.error("Failed to read database!\n\tException: {0}".format(e))
        return None


def get_user_reminders(chat_id: str) -> list:
    """
    Находит все напоминания конкретного пользователя. [(id, chat_id, message_id, reminder_id, date, content)]
    :param chat_id: чат id пользователя.
    :return:
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM reminders WHERE chat_id=?", [chat_id])

        return cursor.fetchall()

    except Exception as e:
        logger.error("Failed to read database!\n\tException: {0}".format(e))
        return None


def get_free_id(chat_id: str) -> int:
    """
    Находит наименьший свободный id для напоминания пользователя.
    :param chat_id: чат id пользователя.
    :return:
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("SELECT reminder_id FROM reminders WHERE chat_id=?", [chat_id])
            data = [x[0] for x in cursor.fetchall()]

        if not data:
            return 1

        for id in range(1, 1000):
            if id not in data:
                return id

        logger.error("Active reminder limit exceeded!")
        return None

    except Exception as e:
        logger.error("Failed to find free id in database!\n\tException: {0}".format(e))
        return None


def add_new(chat_id: str, message_id: str, reminder_id: int, time: str, text: str) -> bool:
    """
    Добавление нового напоминания в DataBase.
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("""INSERT INTO reminders(chat_id, message_id, reminder_id, date, content)
            VALUES (?, ?, ?, ?, ?)""", [chat_id, message_id, reminder_id, time, text])

        return True

    except Exception as e:
        logger.error("Failed to add reminder to database!\n\tException: {0}".format(e))
        return None


def remove(id: int = None, chat_id: str = None):
    """
    Удаляет уведомление с заданным id или удаляет все уведомления определённого пользователя.
    :param id: уведомления, которое необходимо удалить
    :param chat_id: пользователя, все уведомления кторого необходимо удалить
    :return:
    """
    if id and chat_id:
        try:
            with sqlite3.connect(config.data.bot_db) as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM reminders WHERE reminder_id=? AND chat_id=?", [id, chat_id])

            return True

        except Exception as e:
            logger.error("Failed to remove reminder from database!\n\tException: {0}".format(e))
            return None

    elif id:
        try:
            with sqlite3.connect(config.data.bot_db) as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM reminders WHERE id=?", [id])

            return True

        except Exception as e:
            logger.error("Failed to remove reminder from database!\n\tException: {0}".format(e))
            return None

    elif chat_id:
        try:
            with sqlite3.connect(config.data.bot_db) as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM reminders WHERE chat_id=?", [chat_id])

            return True

        except Exception as e:
            logger.error("Failed to remove reminders from database!\n\tException: {0}".format(e))
            return None

    else:
        return None


def edit_time(chat_id: str, reminder_id: int, date: str) -> bool:
    """
    Изменение даты и времени напоминания по его id.
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE reminders SET date=? WHERE chat_id=? AND reminder_id=?""",
                           [date, chat_id, reminder_id])

        return True

    except Exception as e:
        logger.error("Failed to update reminder date in database!\n\tException: {0}".format(e))
        return None


def edit_text(chat_id: str, reminder_id: int, text: str) -> bool:
    """
    Изменение текста напоминания по его id.
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE reminders SET content=? WHERE chat_id=? AND reminder_id=?""",
                           [text, chat_id, reminder_id])

        return True

    except Exception as e:
        logger.error("Failed to update reminder text in database!\n\tException: {0}".format(e))
        return None


def edit_all(chat_id: str, reminder_id: int, date: str, text: str) -> bool:
    """
    Изменение текста напоминания по его id.
    :return: True. None - при вызове исключения.
    """
    try:
        with sqlite3.connect(config.data.bot_db) as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE reminders SET date=?, content=? WHERE chat_id=? AND reminder_id=?""",
                           [date, text, chat_id, reminder_id])

        return True

    except Exception as e:
        logger.error("Failed to update reminder date and text in database!\n\tException: {0}".format(e))
        return None


def reset():
    """
    Полностью удаляет все данные из db.
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
