import logging
import nltk
import re
import datetime

from app.config_reader import load_config


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


def search_day_name(message: str, word: str):
    message = message.lower().split()
    for i in range(len(message)):
        distance = nltk.edit_distance(word.lower(), message[i]) / len(message[i])
        # print(nltk.edit_distance("завтра", word.lower()), distance)

        if distance < 0.6:
            if message[i+1] in ['в']:  # проверка на ненужные символы
                message.pop(i+1)

            message.pop(i)

            if message[i-1] in ['в']:  # проверка на ненужные символы
                message.pop(i-1)

            message = " ".join(message)

            return True, message

    return False, " ".join(message)



