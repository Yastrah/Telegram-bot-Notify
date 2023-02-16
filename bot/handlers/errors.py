import logging

from config.config_reader import load_config

from aiogram import Dispatcher, types
from aiogram.utils.exceptions import BotBlocked, MessageIsTooLong


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def error_catched(update: types.Update, exception):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    # logger.error("User {0} blocked me!\n\tException: {1}".format(update.message.from_user.id, exception))
    logger.error("Found exception with user {0}!\n\tException: {1}".format(update.message.from_user.id, exception))


    if isinstance(exception, MessageIsTooLong):
        await update.message.answer("Сообщение слишком длинное!")
    else:
        await update.message.answer("Возникла какая-то ошибка!")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True

def register_handlers_error(dp: Dispatcher):
    dp.register_errors_handler(error_catched)



