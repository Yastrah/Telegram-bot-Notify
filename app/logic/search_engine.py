import logging
import nltk
import re
import datetime

from app.config_reader import load_config
from app.logic import date_converter


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")

prepositions_list = ['в', 'к']  # автоматически удаляющиеся предлоги


def search_day_name(message: str, word: str) -> (bool, str):
    message = message.lower().split()
    for i in range(len(message)):
        distance = nltk.edit_distance(word.lower(), message[i]) / len(message[i])
        # print(word, distance)

        if distance < 0.5 and i <= 3:
            if message[i+1] in prepositions_list:  # проверка на ненужные символы
                message.pop(i+1)

            message.pop(i)

            if message[i-1] in prepositions_list:  # проверка на ненужные символы
                message.pop(i-1)

            message = " ".join(message)

            return True, message

    return False, " ".join(message)


def search_date(message: str) -> (str, str):
    date_pattern = re.compile("\d{1,2}([-./]\d{1,2})?([-./]\d{2,4})?")
    match = date_pattern.search(message)

    if match and match.start() <= 10:
        date = re.split(r"[-./]", match.group())
        message = message.split()
        i = message.index(match.group())

        if message[i+1] in prepositions_list:  # проверка на ненужные символы
            message.pop(i+1)

        message.pop(i)

        if message[i-1] in prepositions_list:  # проверка на ненужные символы
            message.pop(i-1)

        message = " ".join(message)  # сообщение без даты

        now_date = datetime.datetime.now().strftime(config.logger.date_format)
        now_date = now_date.split()[0].split('/')

        for num in date:
            if len(num) == 1:
                date[date.index(num)] = f"0{num}"
            elif len(num) > 2:
                logger.debug("Reminder handling error!")

        for i in range(len(date), 3):
            date.append(now_date[i])

        if len(date[2]) == 2:
            date[2] = now_date[2][:2] + date[2]

        date = "/".join(date)

        return date, message

    return None, message


def search_time(message: str) -> (str, str):
    time_pattern = re.compile("\d{1,2}([:. /]\d{1,2})?")
    match = time_pattern.search(message)

    if match and match.start() <= 3:
        if len(match.group().split(':')) == 1:
            time = f"{match.group()}:00:00"
        elif len(match.group().split(':')) == 2:
            time = f"{match.group()}:00"
        else:
            time = match.group()

        message = " ".join(message.replace(match.group(), '', 1).split())  # сообщение без времени

        return time, message

    return None, message

