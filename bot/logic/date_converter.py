import logging
import datetime
from config.config_reader import load_config
from config.configuration import Settings


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


def utc(date: str, time_zone: str, mode: str = 't'):
    """
    Переводит дату и время к uts 00 или из него.\n
    :param date: дата в виде словаря.
    :param time_zone: часовой пояс из базы данных.
    :param mode: 't' перевод к uts 00; 'f' перевод из uts 00.
    :return: конвертированная дата формата Settings
    """
    sign, hours, minutes = time_zone[0], int(time_zone[1:3]), int(time_zone[4:])

    if sign == '±':
        return date

    uts_date = datetime.datetime(int(date.split()[0].split('/')[2]), int(date.split()[0].split('/')[1]), int(date.split()[0].split('/')[0]),
                                 int(date.split()[1].split(':')[0]), int(date.split()[1].split(':')[1]))
    if sign == '+' and mode == 't' or sign == '-' and mode == 'f':
        uts_date = (uts_date - datetime.timedelta(hours=hours, minutes=minutes)).strftime(Settings.date_format)
    else:
        uts_date = (uts_date + datetime.timedelta(hours=hours, minutes=minutes)).strftime(Settings.date_format)

    return uts_date

# def from_uts(date: str, time_zone: str):
#     sign, hours, minutes = time_zone[0], int(time_zone[1:3]), int(time_zone[4:])
#
#     uts_date = datetime.datetime(int(date.split()[0].split('/')[2]), int(date.split()[0].split('/')[1]), int(date.split()[0].split('/')[0]),
#                                  int(date.split()[0].split(':')[0]), int(date.split()[0].split(':')[1]))
#     if sign == '+':
#         uts_date = (uts_date + datetime.timedelta(hours=hours, minutes=minutes)).strftime(Settings.date_format)
#     else:
#         uts_date = (uts_date - datetime.timedelta(hours=hours, minutes=minutes)).strftime(Settings.date_format)
#
#     return uts_date


def date_to_value(date: str) -> int:
    """
    Конвертирует строковый формат даты в численное значение. Чем позже дата, тем больше значение.\n
    :param date: дата, формата: день/месяц/год часы:минуты
    :return: численное значение
    """
    date, time = date.split()
    day, month, year = date.split('/')
    hour, minute = time.split(':')
    value = int(year)*10**8 + int(month)*10**6 + int(day)*10**4 + int(hour)*10**2 + int(minute)
    return value


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
    now_date = datetime.datetime.now().strftime(Settings.date_format)

    return now_date.split()[0]


def tomorrow(now_date=datetime.datetime.now().strftime(Settings.date_format)) -> str:
    """
    Обрабатывает все случаи и находит дату для следующего дня.\n
    :param now_date: дата, формата: день/месяц/год
    :return: дата без времени следующего дня.
    """
    date = datetime.datetime.now().strftime(Settings.date_format)
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


def nearest_day_of_the_week(day: str, time_zone: str) -> str:
    """
    Находит дату ближайшего заданного дня недели
    :param day: день недели
    :return: Дата ближайшего нужного дня недели
    """
    days_list = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]

    # date = str(datetime.datetime.today().strftime(Settings.date_format)).split()[0].split('/')
    date = utc(datetime.datetime.utcnow().strftime(Settings.date_format), time_zone, mode='f').split()[0].split('/')

    for i in range(7):
        if datetime.datetime(int(date[2]), int(date[1]), int(date[0])).weekday() == days_list.index(day):
            return f"{date[0]}/{date[1]}/{date[2]}"

        date = (datetime.datetime(int(date[2]), int(date[1]), int(date[0])) + datetime.timedelta(days=1)).strftime("%d/%m/%Y").split('/')

    logger.warning("Couldn't find date for {0}!".format(day))
    return None


def get_day_of_the_week(date: str) -> str:
    """
    Находит день недели заданной даты, возвращая в сокращённом формате.\n
    :param date: дата, формата: день/месяц/год
    :return: день недели формата пн, вт и т.д.
    """
    try:
        date = date.split()[0].split('/')
        day_number = datetime.datetime(int(date[2]), int(date[1]), int(date[0])).weekday()
        return Settings.words_for_week_days[day_number][0]
    except Exception as e:
        logger.debug("Warning: {0}".format(e))
        return None