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


def search_key_word(text: str, words: list, mode: str = 'date') -> (bool, str):
    """
    Поиск соответствия одного из слов в сообщении, заданному.
    :param text: текст сообщения
    :param words: список слов для поиска
    :param mode: тип поиска. Если 'date', то ищет только факт соответствия. Если 'time', то ...
    :return: кортеж, первый элемент отвечает, за то, было ли найдено соответствие, а второй - текст, уже без ключегого слова
    """
    text = text.split()
    for word in words:
        for i in range(len(text)):
            distance = nltk.edit_distance(word.lower(), text[i].lower()) / len(text[i])

            if distance < Settings.day_distance_index and i < Settings.day_order_index:
                if mode == 'date':

                    text.pop(i)
                    # # удаление лишних предлогов
                    # if text[i + 1].lower() in Settings.prepositions_for_delete:
                    #     text.pop(i + 1)
                    #
                    # text.pop(i)
                    #
                    # # удаление лишних предлогов
                    # if text[i - 1].lower() in Settings.prepositions_for_delete:
                    #     text.pop(i - 1)

                    text = " ".join(text)

                    return True, text

                elif mode == 'time':
                    text.pop(i)
                    if text[i - 1].isdigit():
                        text.pop(i - 1)
                        return text[i - 1], text

                    return False, " ".join(text)

    return False, " ".join(text)


def search_date_in_numbers(text: str) -> (str, str):
    """
    Поиск даты в сообщении в численном виде.
    :param text: текст сообщения
    :return: Кортеж: дату в обработанном виде и сообщение без даты. None для првого элемента если ничего не найдено.
    """
    if len(text) < Settings.min_message_len:
        return None, text

    date_pattern = re.compile("\d{1,2}([-./])?(\d{1,2})?([-./])?(\d{2,4})?")
    match = date_pattern.search(text)

    if match and match.start() < Settings.date_order_index:
        found = match.group()
        now_date = datetime.datetime.now().strftime(Settings.date_format).split()[0]

        # если первое сразу задано время
        if text[text.find(found) + len(found)] == ':':
            return now_date, text

        if found[-1] in "-./":
            raise SearchError(f"Match found: {found}",
                              f"Недопустимое формат записи, не ставьте лишние знаки препинания!")

        date = re.split(r"[-./]", found)
        text = ' '.join(text.replace(found, '').split())  # удаление лишних пробелов
        # text = text.split()
        # # print(match.group(), date, text)
        # i = text.index(match.group())
        #
        # # удаление лишних предлогов
        # if text[i + 1].lower() in Settings.prepositions_for_delete:
        #     text.pop(i + 1)
        #
        # text.pop(i)
        #
        # # удаление лишних предлогов
        # if text[i - 1].lower() in Settings.prepositions_for_delete:
        #     text.pop(i - 1)
        #
        # text = " ".join(text)

        now_date = now_date.split('/')

        for i in range(len(date)):
            if len(date[i]) == 1:
                date[i] = '0' + date[i]
            elif len(date[i]) > 2:
                logger.error(f"Reminder handling error! Date: {date}; Text: {text}")
                return None, text

        if not 1 <= len(date) <= 3:
            return None, text

        for i in range(len(date), 3):
            date.append(now_date[i])

        if len(date[2]) == 2:
            date[2] = now_date[2][:2] + date[2]

        date = "/".join(date)

        return date, text, found

    return None, text


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
        time = formatting_time(match.group())
        text = match.group().join(text.split(match.group())[1:]).strip()

        return time, text

    return None, text


def formatting_time(time: str) -> str:
    time = re.split(r"[:./-]", time)

    if not 1 <= len(time) <= 2:
        return None, "Время указано неправильно! введите время напоминания в часах или в час<разделитель(:./)>минута."

    if len(time[0]) == 1:
        time[0] = '0' + time[0]

    for el in time:
        if not len(el) == 2:
            return None, "Вы неправильно указали минуты для времени! Обратите внимание, что для минут надо указать " \
                         "две цифры (например: 05 или 45)"

    if len(time) == 1:
        time = time[0] + ':00'
    elif len(time) == 2:
        time = ':'.join(time)
    else:
        return None, "Вы неправильно указали минуты для времени! Обратите внимание, что для минут надо указать " \
                     "две цифры (например: 05 или 45)"

    if not (0 <= int(time.split(':')[0]) <= 24 and 0 <= int(time.split(':')[1]) <= 59):
        return None, "Вы указали несуществующее время!"

    return time


def date_and_time_handling(text: str) -> tuple:
    """
    Обрабатывает сообщение разбирая его на дату, время и оставшийся текст
    :param text: текст сообщения
    :return:
    """
    date = None

    # поиск и обработка ключевых слов
    found, text = search_key_word(text, ["сегодня"])
    if found:
        date = date_converter.today()

    if date is None:
        found, text = search_key_word(text, ["завтра"])
        if found:
            date = date_converter.tomorrow()

    # поиск и обработка дней недели
    for day in [day[1] for day in Settings.words_for_week_days]:
        found, text = search_key_word(text, day)
        if found:
            date = date_converter.nearest_day_of_the_week(day)
            break

    # поиск и обработка месяца ввиде слова
    for month, word in enumerate(Settings.words_for_months):
        found, text = search_key_word(text, word)
        if found:
            now_year = datetime.datetime.now().strftime("%Y")
            day, text = search_first_number(text)
            if not day:
                raise SearchError(f"Could not find day for month {month+1}",
                                  f"Не удалось найти день для месяца {word} в сообщении!")

            if month+1 < 10:
                date = f"{day}/0{month+1}/{now_year}"
            else:
                date = f"{day}/{month+1}/{now_year}"
            break



    # поиск даты в числовом виде, если не нашлось ключевых слов
    if date is None:
        date, text, found = search_date_in_numbers(text)

    if date is None:
        return None, None, None

    # поиск времени
    time, text = search_time(text)

    if time is None:
        date = datetime.datetime.now().strftime(Settings.date_format).split()[0]
        time = formatting_time(found)
        # print("found: ", found)

    return date, time, text
