class Settings:
    """
    Класс, хранящий в себе все настраиваемые коэффициенты и вспомогательные данные.
    """
    date_format = "%d/%m/%Y %H:%M"

    with open("data/blocked_users.txt", mode='r', encoding="utf-8") as file:
        blocked_users = list(map(int, file.read().split('\n')[:-1]))

    words_for_week_days = [["пн", ["понедельник"]], ["вт", ["вторник"]], ["ср", ["среда"]], ["чт", ["четверг"]],
                           ["пт", ["пятница"]], ["сб", ["суббота"]], ["вс", ["воскресенье"]]]
    words_for_months = [["январь"], ["февраль"], ["март"], ["апрель"], ["май"], ["июнь"], ["июль"], ["август"],
                        ["сентябрь"], ["октябрь"], ["ноябрь"], ["декабрь"]]
    words_for_time = [["час", "часа", "часов"], ["минута", "минуты", "минут", "мин"]]

    prepositions_for_delete = ['в', 'во', 'к', 'с']  # автоматически удаляющиеся предлоги

    min_message_len = 6  # минимальная длина сообщения, допустимая для обработки
    day_distance_index = 0.5  # коэффициент допустимой погрешности(опечаток) в ключевых словах
    day_order_index = 3  # наиболее дальнее(не включая) расположение ключевого слова от начала строки(по номеру слова)
    date_order_index = 10  # наиболее дальнее(не включая) расположение даты от начала строки(по номеру символа)
    time_order_index = 4  # наиболее дальнее(не включая) расположение времени от начала строки(по номеру символа)

    max_reports_per_day = 3  # наибольшее разрешённое число жалоб от одного пользователя в день

    callback_utc_data = [
        'utc -10:00', 'utc -09:00', 'utc -08:00', 'utc -07:00',
        'utc -06:00', 'utc -05:00', 'utc -04:00', 'utc -03:00',
        'utc -02:00', 'utc -01:00', 'utc ±00:00', 'utc +01:00',
        'utc +02:00', 'utc +03:00', 'utc +04:00', 'utc +05:00',
        'utc +06:00', 'utc +07:00', 'utc +08:00', 'utc +09:00',
        'utc +10:00', 'utc +11:00', 'utc +12:00', 'utc +13:00',
    ]

class Constants:
    """
    Содержит константные строки для команд и сообщений.
    """
    # Emojis used ⚡️🔒 🔻 🔔 📃 🗑 ↩ ✏ ◀️📅 🏠 ✅ ❌ 🕑 📝 ❗ • ⚙

    user_commands = {
        "start": {
            "description": "начать пользоваться",
            "text": {"ru": "📅 Привет!\nЯ <u><b>{bot_name}</b>!</u> Буду напоминать тебе о твоих делах.\n\n"
                           "⚡️ Для удобства использования рекомендуется <u><b>закрепить</b></u> чат с ботом и поставить "
                           "<u><b>отдельный звук</b></u> для сообщений от бота.\n\n"
                           "Для создания напоминания отправьте сообщение в котором <u><b>в начале стоит дата</b></u> в виде: "
                           "'сегодня', 'завтра', любого дня недели или в численном формате с разделителями <b>(-./)</b>; "
                           "<u><b>потом время</b></u> с указанием часа или вместе с минутами через разделитель <b>(:./-)</b>; "
                           "<u><b>вся оставшаяся часть сообщения станет напоминанием</b></u>.\n\n"
                           "Чтобы подробнее узнать как пользоваться ботом, воспользуйтесь командой /help\n\n"
                           "<i>Разработано Yastrah.</i>",
                     "en": "Hi!\nI'm <u><b>{bot_name}</b>!</u>\nDesigned by Yastrah."},
        },
        "help": {
            "description": "помощь в использовании бота",
            "text": {"ru": "<b>{bot_name}</b> - это бот позволяющий создавать напоминания без строгого формата.\n\n"
                           "⚡️ Чтобы создать новое напоминание, отправьте любое сообщение <b>в свободном формате</b>, "
                           "главное в <b>начале укажите дату</b> (только день или день вместе с месяцем) или день недели, "
                           "<b>потом время</b>, когда должно придти напоминание(можно с указанием минут или без них), и "
                           "всё <b>оставшееся сообщение будет текстом вашего напоминания</b>.\n\n"
                           "Вот несколько примеров:\n"
                           "- завтра в 14 не забыть отправить посылку\n"
                           "- сегодня 12.41 сходить в магазин\n"
                           "- суббота в 19/30 посмотреть фильм\n"
                           "- 25 10:30 поздравить друга с днем рождения\n"
                           "- в воскресенье в 11-20 не забыть оплатить подписку\n"
                           "- 4.07.23 12:40 поздравить начальника\n"
                           "- 25.05 в 13.30 через час быть на собеседовании\n\n"
                           "• Если вы хотите посмотреть список всех текущих напоминаний с их номерами, временем и текстом, "
                           "воспользуйтесь командой /list или кнопкой <b>📃 список</b>.\n"
                           "• Для удаления напоминания по номеру используйте команду /delete или кнопку "
                           "<b>🗑 удалить</b>.\n"
                           "• Чтобы изменить время или содержимое напоминания воспользуйтесь командой /edit или "
                           "кнопкой <b>✏️ изменить</b>.\n"
                           "• Если вы хотите быстро удалить последнее напоминания введите команду /undo или нажмите кнопку "
                           "<b>↩️ отменить</b>.\n\n"
                           "❗ Если вы нашли какую-то ошибку/недоработку или у вас есть идея, как сделать бота лучше, "
                           "пожалуйста воспользуйтесь командой /report.", "en": None},
        },
        "settings": {
            "description": "персональные настройки",
            "text": {"ru": "⚙ Настройки\n"
                           "Вы были зарегистрированы <b>{registered}</b>.\n"
                           "За всё время вам было отправлено <b>{reminders_sent}</b> напоминаний.\n"
                           "Часовой пояс: <b>{time_zone}</b>\n"
                           "Язык: <b>{language}</b>", "en": None},
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
            "custom_name": "↩ отменить",
        },
        "edit": {
            "description": "изменинить текст напоминания по id",
            "custom_name": "✏ изменить",
        },
        "menu": {
            "description": "вернуться в главное меню",
            "custom_name": "🏠 меню",
        },
        "report": {
            "description": "пожаловаться на ошибку / предложить доработки",
            "what_to_do": {"ru": "Введите, как можно более подробный, текст обращения:", "en": None},
            "report_saved": {"ru": "Ваше сообщение успешно сохранено с id <b>{report_id}</b>", "en": None},
            "too_many_reports": {"ru": "Вы за сегодня уже отправили максимальное допустимое число жалоб/предложений "
                                       "<b>({max_reports_per_day})</b>!", "en": None},
        },
    }

    settings_text = {
        "please_select_utc": {"ru": "Пожалуйста выберите свой часовой пояс, сделать это можно под сообщением о "
                                    "выборе пояса или в настройках (/settings)!", "en": None},
        "selecting_utc": {"ru": "🕑 Пожалуйста, выберите свой <b>часовой пояс</b>, нажав под сообщением на нужное отклонение "
                                "от <u><b>UTS 00:00</b></u>!\n\n"
                                "Если в месте вашего проживания предусмотрен переход на <b>летнее время</b>, "
                                "не забывайте менять часовой пояс в настройках /settings.", "en": None},
        "utc_set": {"ru": "Часовой пояс успешно установлен на <u><b>UTC {time_zone}</b></u>", "en": None},
    }

    # please_select_utc = "Пожалуйста выберите свой часовой пояс, сделать это можно под сообщением о регистрации или в " \
    #                     "настройках (/settings)!"
    # registration_message = "регистрация"
    # select_uts_message = "установка uts"
    # select_language_message = "установка языка"

