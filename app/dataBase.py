import json
import logging
import datetime
from app.config_reader import load_config

logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


def read() -> list:
    """
    Получение данных из db.\n
    :return: Данные в виде списка словарей (list). None - при вызове исключения.
    """
    try:
        with open(r"data\notifications.json", "r") as file:
            data: dict = json.load(file)
            return data

    except Exception as e:
        logger.error("Failed to read DataBase!\n\tException: {0}".format(e))
        return None


def get_now(time) -> list:
    """
    Получение данных из db.\n
    :return: Данные в виде списка словарей (list). None - при вызове исключения.
    """
    try:
        with open(r"data\notifications.json", "r") as file:
            data: dict = json.load(file)

        answer = []
        for chat, notifications in data:
            for message in notifications:
                if message.get("time") == time:
                    answer.append({"chat_id": chat, "time": message.get("time"), "text": message.get("text")})

        return answer

    except Exception as e:
        logger.error("Failed to read DataBase!\n\tException: {0}".format(e))
        return None


def add_new(time: str, chat_id: int, text: str) -> bool:
    """
    Получение данных из db.\n
    :return: Данные в виде списка словарей (list). None - при вызове исключения.
    """
    try:
        with open(r"data\notifications.json", "r") as file:
            data: dict = json.load(file)
        data[chat_id].append({"time": time, "text": text})

        with open(r"data\notifications.json", "w") as file:
            json.dump(data, file)


    except Exception as e:
        logger.error("Failed to add notification to DataBase!\n\tException: {0}".format(e))
        return None


def reset() -> bool:
    """
    Полностью удаляет все данные из db.\n
    :return: True - при успешном добавлениии, False - при вызове исключения.
    """
    # now_time = datetime.datetime.now().strftime(config.logger.date_format)

    # default = dict(last_update=now_time, users=0, teams=[])

    try:
        with open("characters.json", "w") as file:
            json.dump({}, file)
            return True

    except Exception as e:
        logger.error("Failed to read db!\n\tException: {0}".format(e))
        return False
