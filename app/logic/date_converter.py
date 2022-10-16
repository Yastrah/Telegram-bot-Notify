import logging
import datetime
from app.config_reader import load_config


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")

def dict_in_date(old_date: dict) -> str:
    """
    Переводит словарь со значениями int в строку, нужного формата.\n
    :param old_date: дата в виде словаря.
    :return: полная дата str.
    """

    date = ""
    if len(str(old_date["day"])) == 1:
        date += '0'
    date += "{0}/".format(old_date["day"])

    if len(str(old_date["month"])) == 1:
        date += '0'
    date += "{0}/".format(old_date["month"])

    if len(str(old_date["year"])) == 1:
        date += '0'
    date += "{0} ".format(old_date["year"])

    if len(str(old_date["hour"])) == 1:
        date += '0'
    date += "{0}:".format(old_date["hour"])

    if len(str(old_date["minute"])) == 1:
        date += '0'
    date += "{0}:".format(old_date["minute"])

    date += "00"

    return date


def today() -> str:
    """
    Находит текущую дату.\n
    :return: текущая дата без времени.
    """
    now_date = datetime.datetime.now().strftime(config.logger.date_format)

    return now_date.split()[0]


def tomorrow(now_date=datetime.datetime.now().strftime(config.logger.date_format)) -> str:
    """
    Обрабатывает все случаи и находит дату для следующего дня.\n
    :param now_date: строка, формата: день/месяц/год
    :return: дата без времени следующего дня.
    """
    date = datetime.datetime.now().strftime(config.logger.date_format)
    if now_date != date:
        now_date += " "+str(date.split()[1])

    now_date = {"day": int(now_date.split()[0].split("/")[0]), "month": int(now_date.split()[0].split("/")[1]),
                "year": int(now_date.split()[0].split("/")[2]), "hour": int(now_date.split()[1].split(":")[0]),
                "minute": int(now_date.split()[1].split(":")[1]), "second": 0}

    if now_date["month"] in (4, 6, 9, 11) and now_date["day"] == 30:  # месяца по 30 дней
        now_date["month"] += 1
        now_date["day"] = 1

    elif now_date["month"] in (1, 3, 5, 7, 8, 10) and now_date["day"] == 31:  # месяца по 31 дней
        now_date["month"] += 1
        now_date["day"] = 1

    elif now_date["month"] == 12 and now_date["day"] == 31:  # последний день года
        now_date["year"] += 1
        now_date["month"] = 1
        now_date["day"] = 1

    elif now_date["month"] == 2 and now_date["year"] % 4 == 0 and now_date["day"] == 28:  # високосный февраль
        now_date["month"] += 1
        now_date["day"] = 1

    elif now_date["month"] == 2 and now_date["year"] % 4 != 0 and now_date["day"] == 29:  # невисокосный февраль
        now_date["month"] += 1
        now_date["day"] = 1

    else:
        now_date["day"] += 1

    return dict_in_date(now_date).split()[0]


def day_of_the_week(day: str) -> str:
    """
    Находит дату ближайшего заданного дня недели
    :param day: день недели
    :return: Дата ближайшего нужного дня недели
    """
    days_list = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]

    date = str(datetime.datetime.today().strftime(config.logger.date_format)).split()[0].split('/')
    # print(tomorrow(f"{date[0]}/{date[1]}/{date[2]}"))
    for i in range(7):
        if datetime.datetime(int(date[2]), int(date[1]), int(date[0])).weekday() == days_list.index(day):
            return f"{date[0]}/{date[1]}/{date[2]}"

        date = tomorrow(f"{date[0]}/{date[1]}/{date[2]}").split('/')

    logger.warning("Couldn't find date for {0}!".format(day))
    return None
