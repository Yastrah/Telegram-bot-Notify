class Settings(object):
    """
    Класс, хранящий в себе все настраиваемые коэффициенты и вспомогательные данные.
    """
    # @staticmethod
    # def func():
    #     print("Hi")

    week_days = [["пн", "понедельник"], ["вт", "вторник"], ["ср", "среда"], ["чт", "четверг"],
                 ["пт", "пятница"], ["сб", "суббота"], ["вс", "воскресенье"]]

    prepositions_for_delete = ['в', 'во', 'к', 'с', 'd', 'dj', 'r', 'c']  # автоматически удаляющиеся предлоги

    day_distance_index = 0.5  # коэффициент допустимой погрешности(опечаток) в ключевых словах
    day_order_index = 3  # наиболее дальнее(не включая) расположение ключевого слова от начала строки(по номеру слова)
    date_order_index = 10  # наиболее дальнее(не включая) расположение даты от начала строки(по номеру символа)
    time_order_index = 4  # наиболее дальнее(не включая) расположение времени от начала строки(по номеру символа)


class Constants(object):
    """
    Содержит константные строки для команд и сообщений.
    """
    user_commands = {
        "start": {
            "description": "начать пользоваться",
            "text": {"ru": None, "en": "Hi!\nI'm <u><b>{0}</b>!</u>\nDesigned by Yastrah."},
        },
        "help": {
            "description": "помощь в использовании бота",
            "text": {"ru": "<b>{0}</b> - это бот позволяющий создавать напоминания.\nКомады:\n...", "en": None},
        },
        "list": {
            "description": "вывод всех активных напоминаний",
            # "text": {"ru": "<b>{0}</b> - это бот позволяющий создавать напоминания.\nКомады:\n...", "en": None},
        },
    }
