class Settings(object):
    """
    Класс, хранящий в себе все настраиваемые коэффициенты и вспомогательные данные.
    """
    date_format = "%d/%m/%Y %H:%M"

    with open("data/blocked_users.txt", mode='r', encoding="utf-8") as file:
        blocked_users = list(map(int, file.read().split('\n')[:-1]))

    week_days = [["пн", "понедельник"], ["вт", "вторник"], ["ср", "среда"], ["чт", "четверг"],
                 ["пт", "пятница"], ["сб", "суббота"], ["вс", "воскресенье"]]

    prepositions_for_delete = ['в', 'во', 'к', 'с', 'd', 'dj', 'r', 'c']  # автоматически удаляющиеся предлоги

    min_messege_len = 6  # минимальная длина сообщения, допустимая для обработки
    day_distance_index = 0.5  # коэффициент допустимой погрешности(опечаток) в ключевых словах
    day_order_index = 3  # наиболее дальнее(не включая) расположение ключевого слова от начала строки(по номеру слова)
    date_order_index = 10  # наиболее дальнее(не включая) расположение даты от начала строки(по номеру символа)
    time_order_index = 4  # наиболее дальнее(не включая) расположение времени от начала строки(по номеру символа)

    max_reports_per_day = 3  # наибольшее разрешённое число жалоб от одного пользователя в вень


class Constants(object):
    """
    Содержит константные строки для команд и сообщений.
    """
    # Emojis used ⚡️ 🔒 🔻 🔔 📃 🗑 ↩️ ✏️ ◀️ 📅 🏠 ✅ ❌ 🕑 📝

    user_commands = {
        "start": {
            "description": "начать пользоваться",
            "text": {"ru": "Привет!\nЯ <u><b>{bot_name}</b>!</u> Буду напоминать тебе о твоих делах.\n\n"
                           "Для создания напоминания отправьте сообщение в котором <u><b>в начале стоит дата</b></u> в виде: "
                           "'сегодня', 'завтра', любого дня недели или в численном формате с разделителями <b>(-./)</b>; "
                           "<u><b>потом время</b></u> с указанием часа или вместе с минутами через разделитель <b>(:./-)</b>; "
                           "<u><b>вся оставшаяся часть сообщения станет напоминанием</b></u>.\n\n"
                           "Чтобы подробнее узнать как пользоваться ботом, воспользуйтесь командой <b>/help</b>\n\n"
                           "Разработано Yastrah.",
                     "en": "Hi!\nI'm <u><b>{bot_name}</b>!</u>\nDesigned by Yastrah."},
        },
        "help": {
            "description": "помощь в использовании бота",
            "text": {"ru": "<b>{bot_name}</b> - это бот позволяющий создавать напоминания без строгого формата.\n"
                           "Чтобы создать новое напоминание, отправьте любое сообщение <b>в свободном формате</b>, "
                           "главное в <b>начале укажите дату</b> (только день или день вместе с месяцем) или день недели, "
                           "<b>потом время</b>, когда должно придти напоминание(можно с указанием минут или без них), и "
                           "всё <b>оставшееся сообщение будет текстом вашего напоминания</b>.\n\n"
                           "Вот несколько примеров:\n"
                           "- завтра в 14 не забыть отправить посылку\n"
                           "- сегодня 12.41 сходить в магазин\n"
                           "- суббота в 19/30 посмотреть фильм\n"
                           "- 25 10:30 поздравить друга с днем рождения\n"
                           "- в воскресенье в 11-20 не забыть оплатить подписку\n"
                           "- 25.05 в 13.30 через час быть на собеседовании\n\n"
                           "Если вы хотите посмотреть список всех текущих напоминаний с их номерами, временем и текстом, "
                           "воспользуйтесь командой <b>/list</b> или кнопкой <b>📃 список</b>.\n"
                           "Для удаления напоминания по номеру используйте команду <b>/delete</b> или кнопку "
                           "<b>🗑 удалить</b>.\n"
                           "Чтобы изменить время или содержимое напоминания воспользуйтесь командой <b>/edit</b> или "
                           "кнопкой <b>✏️ изменить</b>.\n"
                           "Если вы хотите быстро удалить последнее напоминания введите команду <b>/undo</b> или нажмите кнопку "
                           "<b>↩️ отменить</b>.\n\n"
                           "Если вы нашли какую-то ошибку/недоработку или у вас есть идея, как сделать бота лучше, "
                           "пожалуйста воспользуйтесь командой <b>/report</b>."
                           "", "en": None},
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
        "menu": {
            "description": "вернуться в главное меню",
            "custom_name": "🏠 меню",
        },
        "report": {
            "description": "пожаловаться на ошибку / предложить доработки",
            "what_to_do": {"ru": "Введите, как можно более подробный, текст обращения:",
                           "en": None},
            "report_saved": {"ru": "Ваше сообщение успешно сохранено",
                             "en": None},
            "too_many_reports": {"ru": "Вы за сегодня уже отправили максимальное допустимое число жалоб/предложений "
                                       "({max_reports_per_day})!",
                                       "en": None},
        },
    }




