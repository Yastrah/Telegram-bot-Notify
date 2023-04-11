import logging

import nltk
import re
import datetime

from config.config_reader import load_config
from config.configuration import Settings

from bot.handlers.errors import SearchError
from bot.logic import date_converter

logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


def word_matches(text: str, words: list) -> bool:
    """
    Соответствует ли слово какому-либо из переданного списка.
    :param text: текст сообщения.
    :param words: список слов для поиска.
    :return: Bool - соответствует слово или нет
    """
    for word in words:
        distance = nltk.edit_distance(word.lower(), text.lower()) / len(text)

        if distance < Settings.day_distance_index:
            return True

    return False


def search_key_word(text: str, words: list, mode: str = 'date') -> (bool, str):
    """
    Поиск соответствия одного из слов в сообщении, заданному.
    :param text: текст сообщения.
    :param words: список слов для поиска.
    :param mode: тип поиска. Если 'date', то ищет только факт соответствия. Если 'time', то ...
    :return: кортеж, первый элемент отвечает, за то, было ли найдено соответствие, а второй - текст, уже без ключегого слова
    """
    text = text.split()

    for i in range(len(text)):
        if word_matches(text[i], words) and i < Settings.day_order_index:
            if mode == 'date':
                return True, " ".join(text[i+1:])

            elif mode == 'time':
                if text[i - 1].isdigit():
                    return text[i - 1], " ".join(text[i+1:])

                return None, " ".join(text)

    return None, " ".join(text)


def search_date_in_numbers(text: str, time_zone: str) -> (str, str, str):
    """
    Поиск даты в сообщении в численном виде.
    :param text: текст сообщения.
    :param time_zone: часовой пояс.
    :return: Кортеж: дату в обработанном виде и сообщение без даты. None для првого элемента если ничего не найдено.
    """
    if len(text) < Settings.min_message_len:
        return None, text,None

    date_pattern = re.compile("\d{1,2}([-./])?(\d{1,2})?([-./])?(\d{2,4})?")
    match = date_pattern.search(text)

    if match and match.start() < Settings.date_order_index:
        found = match.group()
        now_date = (date_converter.utc(datetime.datetime.utcnow().strftime(Settings.date_format), time_zone, mode='f')).split()[0]

        # если первое сразу задано время
        if text[text.find(found) + len(found)] == ':':
            return now_date, text, None
        if word_matches(text.split(found)[1].strip().split()[0], Settings.words_for_time[0]+Settings.words_for_time[1]):
            return now_date, text, None

        if found[-1] in "-./":
            raise SearchError(f"Match found: {found}",
                              f"Недопустимое формат записи, не ставьте лишние знаки препинания!")

        date = re.split(r"[-./]", found)
        text = text[text.find(found) + len(found):].strip()

        now_date = now_date.split('/')

        for i in range(len(date)):
            if len(date[i]) == 1:
                date[i] = '0' + date[i]
            elif len(date[i]) > 2:
                logger.error(f"Reminder handling error! Date: {date}; Text: {text}")
                return None, text, found

        if not 1 <= len(date) <= 3:
            return None, text, found

        for i in range(len(date), 3):
            date.append(now_date[i])

        if len(date[2]) == 2:
            date[2] = now_date[2][:2] + date[2]

        date = "/".join(date)

        return date, text, found

    return None, text, None


def search_first_number(text: str) -> (str, str):
    """
    Ищет первое число в строке.
    :param text: текст сообщения
    :return: Кортеж: найденное число и сообщение без этого числа. None для првого элемента если ничего не найдено.
    """
    match = re.search(r"\d{1,2}", text)
    if match and match.start() < Settings.date_order_index:
        text = ' '.join(text.replace(match.group(), '').split())  # удаление лишних пробелов
        return match.group(), text

    return None, text


def search_time(text: str) -> (str, str):
    """
    Поиск времени в сообщении.
    :param text: текст сообщения
    :return: Кортеж: время в обработанном виде и сообщение без него. None для првого элемента если ничего не найдено.
    """
    time_pattern = re.compile(r"\d{1,2}([:./]\d{1,2})?")
    match = time_pattern.search(text)

    if match and match.start() < Settings.time_order_index:
        found = match.group()
        time = formatting_time(found)
        text = found.join(text.split(found)[1:]).strip()
        # print(text.find(found)+len(found))
        # text = text[text.find(found)+len(found):].strip()  # удаление лишних пробелов

        return time, text

    return None, text


def formatting_time(time: str) -> str:
    """
    Обработка найденного времени. Приведение к стандартному формату.
    :param time: найденное время.
    :return: Отформатированное время
    """
    time = re.split(r"[:./-]", time)

    if not 1 <= len(time) <= 2:
        raise SearchError(f"Time length is not correct: {time}",
                          "Время указано неправильно! введите время напоминания в часах или в час<разделитель(:./)>минута.")
        # return None, "Время указано неправильно! введите время напоминания в часах или в час<разделитель(:./)>минута."

    if len(time[0]) == 1:
        time[0] = '0' + time[0]

    for el in time:
        if not len(el) == 2:
            raise SearchError(f"Time minutes length is not correct: {time}",
                              "Вы неправильно указали минуты для времени! Обратите внимание, что для минут надо указать"
                              " две цифры (например: 05 или 45)")
            # return None, "Вы неправильно указали минуты для времени! Обратите внимание, что для минут надо указать " \
            #              "две цифры (например: 05 или 45)"

    if len(time) == 1:
        time = time[0] + ':00'
    elif len(time) == 2:
        time = ':'.join(time)
    # else:
    #     raise SearchError(f"Time minutes length is not correct: {time}",
    #                       "Вы неправильно указали минуты для времени! Обратите внимание, что для минут надо указать две"
    #                       " цифры (например: 05 или 45)"
    # return None, "Вы неправильно указали минуты для времени! Обратите внимание, что для минут надо указать " \
    #              "две цифры (например: 05 или 45)"

    if not (0 <= int(time.split(':')[0]) <= 24 and 0 <= int(time.split(':')[1]) <= 59):
        raise SearchError(f"Time minutes length is not correct: {time}",
                          "Вы указали несуществующее время!")
        # return None, "Вы указали несуществующее время!"

    return time


def date_and_time_handling(text: str, time_zone: str) -> tuple:
    """
    Обрабатывает сообщение разбирая его на дату, время и оставшийся текст.
    :param text: текст сообщения.
    :param time_zone: часовой пояс.
    :return: дата, время, текст
    """
    found, text = search_key_word(text, ["через"])
    if found:

        # поиск ключевых слов для времени
        hours, text = search_key_word(text, Settings.words_for_time[0], mode='time')
        minutes, text = search_key_word(text, Settings.words_for_time[1], mode='time')

        # поиск времени в численном виде
        if hours is None and minutes is None:
            time, text = search_time(text)
            hours, minutes = time.split(':')

        if hours is None:
            hours = '00'

        if minutes is None:
            minutes = '00'

        hours, minutes = int(hours), int(minutes)

        now_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=hours, minutes=minutes)).strftime(Settings.date_format)
        full_date = date_converter.utc(now_date, time_zone, mode='f')
        date, time = full_date.split()[0], full_date.split()[1]
        return date, time, text

    date = None

    # поиск и обработка ключевых слов
    if date is None:
        found, text = search_key_word(text, ["сегодня"])
        if found:
            # date = date_converter.today()
            date = date_converter.utc(datetime.datetime.utcnow().strftime(Settings.date_format),
                                      time_zone, mode='f').split()[0]

    if date is None:
        found, text = search_key_word(text, ["послезавтра"])
        if found:
            now_date = (datetime.datetime.utcnow() + datetime.timedelta(days=2)).strftime(Settings.date_format)
            date = date_converter.utc(now_date, time_zone, mode='f').split()[0]

    if date is None:
        found, text = search_key_word(text, ["завтра"])
        if found:
            # date = date_converter.tomorrow()
            now_date = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime(Settings.date_format)
            date = date_converter.utc(now_date, time_zone, mode='f').split()[0]

    # поиск и обработка дней недели
    for day in [day[1] for day in Settings.words_for_week_days]:
        found, text = search_key_word(text, day)
        if found:
            date = date_converter.nearest_day_of_the_week(day[0], time_zone)
            break

    # поиск и обработка месяца в виде слова
    for month, word in enumerate(Settings.words_for_months):
        found, text = search_key_word(text, word, mode='time')
        if found:
            now_year = (date_converter.utc(datetime.datetime.utcnow().strftime(Settings.date_format), time_zone, mode='f')).split()[0].split('/')[2]
            day = found
            if not day:
                raise SearchError(f"Could not find day for month {month + 1}",
                                  f"Не удалось найти день для месяца {word} в сообщении!")

            if month + 1 < 10:
                date = f"{day}/0{month + 1}/{now_year}"
            else:
                date = f"{day}/{month + 1}/{now_year}"
            break

    # поиск даты в числовом виде, если не нашлось ключевых слов
    if date is None:
        date, text, found = search_date_in_numbers(text, time_zone)

    if date is None:
        return None, None, None

    # поиск ключевых слов для времени
    time = None
    hours, text = search_key_word(text, Settings.words_for_time[0], mode='time')
    if hours:
        minutes, text = search_key_word(text, Settings.words_for_time[1], mode='time')
        if minutes:
            time = f"{hours}:{minutes}"
        else:
            time = f"{hours}:00"

    # поиск времени в численном виде
    if time is None:
        time, text = search_time(text)

    if time is None and found is None:
        raise SearchError(f"Could not find time in message: {text}",
                          "Не удалось обработать дату и время!")

    # если время не найдено, то дата превращается во время, а дата ставится сегодняшняя
    if time is None:
        if not 1 <= len(re.split(r"[:./-]", found)) <= 2:
            raise SearchError(f"Time length is not correct: {found}",
                              "Время указано неправильно! введите время напоминания в часах или в час<разделитель(:./)>минута.")

        date = (date_converter.utc(datetime.datetime.utcnow().strftime(Settings.date_format), time_zone, mode='f')).split()[0]
        time = formatting_time(found)

    return date, time, text
