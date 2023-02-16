import logging
import nltk
import re
import datetime

from config.config_reader import load_config
from config.configuration import Settings


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


def search_day_name(text: str, word: str) -> (bool, str):
    text = text.split()
    for i in range(len(text)):
        distance = nltk.edit_distance(word.lower(), text[i].lower()) / len(text[i])

        if distance < Settings.day_distance_index and i < Settings.day_order_index:
            if text[i + 1].lower() in Settings.prepositions_for_delete:
                text.pop(i + 1)

            text.pop(i)

            if text[i - 1].lower() in Settings.prepositions_for_delete:
                text.pop(i - 1)

            text = " ".join(text)

            return True, text

    return False, " ".join(text)


def search_date(text: str) -> (str, str):
    date_pattern = re.compile("\d{1,2}([-./]\d{1,2})?([-./]\d{2,4})?")
    match = date_pattern.search(text)

    if match and match.start() < Settings.date_order_index:
        date = re.split(r"[-./]", match.group())
        text = text.split()
        i = text.index(match.group())

        if text[i + 1].lower() in Settings.prepositions_for_delete:
            text.pop(i + 1)

        text.pop(i)

        if text[i - 1].lower() in Settings.prepositions_for_delete:
            text.pop(i - 1)

        text = " ".join(text)

        now_date = datetime.datetime.now().strftime(Settings.date_format)
        now_date = now_date.split()[0].split('/')

        for num in date:
            if len(num) == 1:
                date[date.index(num)] = f"0{num}"
            elif len(num) > 2:
                logger.warning("Reminder handling error!")

        if not 1 <= len(date) <= 3:
            return None, text

        for i in range(len(date), 3):
            date.append(now_date[i])

        if len(date[2]) == 2:
            date[2] = now_date[2][:2] + date[2]

        date = "/".join(date)

        return date, text

    return None, text


def search_time(text: str) -> (str, str):
    time_pattern = re.compile(r"\d{1,2}([:./]\d{1,2})?")
    match = time_pattern.search(text)

    if match and match.start() < Settings.time_order_index:
        time = re.split(r"[:./]", match.group())

        if not 1 <= len(time) <= 2:
            return None, "Время указано неправильно! введите время напоминания в часах или в час<разделитель(:./)>минута."

        for el in time[1:]:
            if not len(el) == 2:
                return None, "Вы неправильно указали минуты для времени! Обратите внимание, что для минут надо указать " \
                             "две цифры (например: 05 или 45)"

        if len(time) == 1:
            time = time[0] + ':00'
        elif len(time) == 2:
            time = ':'.join(time)

        if not (0 <= int(time[:2]) <= 24 and 0 <= int(time[3:]) <= 59):
            return None, "Вы указали несуществующее время!"

        text = match.group().join(text.split(match.group())[1:]).strip()

        return time, text

    return None, text

