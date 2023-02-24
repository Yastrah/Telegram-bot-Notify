class Settings(object):
    """
    Класс, хранящий в себе все настраиваемые коэффициенты и вспомогательные данные.
    """
    date_format = "%d/%m/%Y %H:%M"
    blocked_users = [740736853, ]
    week_days = [["пн", "понедельник"], ["вт", "вторник"], ["ср", "среда"], ["чт", "четверг"],
                 ["пт", "пятница"], ["сб", "суббота"], ["вс", "воскресенье"]]

    prepositions_for_delete = ['в', 'во', 'к', 'с', 'd', 'dj', 'r', 'c']  # автоматически удаляющиеся предлоги

    min_messege_len = 6  # минимальная длина сообщения, допустимая для обработки
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
            "text": {"ru": "Привет!\nЯ <u><b>{bot_name}</b>!</u> Буду напоминать тебе о твоих делах.\n\n"
                           "Для создания напоминания отправьте сообщение в котором в начале стоит <u><b>дата</b></u> в виде: "
                           "'сегодня', 'завтра', любого дня недели или в численном формате с разделителями <b>(-./)</b>; "
                           "<u><b>потом время</b></u> с указанием часа или вместе с минутами через разделитель <b>(:./)</b>; "
                           "<u><b>вся оставшаяся часть сообщения станет напоминанием</b></u>.\n\n"
                           "Чтобы подробнее узнать как пользоваться ботом, воспользуйтесь командой <b>/help</b>\n\n"
                           "Разработано Yastrah.",
                     "en": "Hi!\nI'm <u><b>{bot_name}</b>!</u>\nDesigned by Yastrah."},
        },
        "help": {
            "description": "помощь в использовании бота",
            "text": {"ru": '<b>{bot_name}</b> - это бот позволяющий создавать напоминания.\n'
                           'Если вы хотите посмотреть все текущие напоминания, воспользуйтесь командой <b>/list</b> или кнопкой <b>📃список</b>\n\n'
                           'Чтобы создать новое напоминание, отправьте любое сообщение <b>в свободном формате</b>, '
                           'главное в <b>начале укажите дату</b> (только день или день вместе с месяцем) или день недели, '
                           '<b>потом время</b>, когда должно придти напоминание(можно с указанием минут или без них), и '
                           'всё <b>оставшееся сообщение будет текстом вашего напоминания</b>.\n\n'
                           'Вот несколько примеров напоминаний:\n'
                           '"завтра в 14 не забыть отправить посылку";\n"сегодня 12.41 сходить в магазин";\n'
                           '"суббота в 19/30 посмотреть фильм";\n"25 10:30 поздравить друга с днем рождения";\n'
                           '"в воскресенье в 11 не забыть оплатить подписку".', "en": None},
        },
        "list": {
            "description": "вывод всех активных напоминаний",
            "custom_name": "📃 список",
        },
        "delete": {
            "description": "удаление напоминания по id",
            "custom_name": "🗑 удалить",
        },
        "undo": {
            "description": "удаление последнего созданного напоминания",
            "custom_name": "↩️ отменить",
        },
        "edit": {
            "description": "изменинить текст напоминания по id",
            "custom_name": "✏️ изменить",
        },
        "cancel": {
            "description": "сбросить состояние",
            "custom_name": "◀️ назад",
        },
    }




