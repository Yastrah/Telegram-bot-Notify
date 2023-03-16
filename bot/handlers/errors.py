import logging

from config.config_reader import load_config
from bot.db import reminders, users

from aiogram import Dispatcher, types
from aiogram.utils.exceptions import BotBlocked, MessageIsTooLong, CantParseEntities


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


class SearchError(Exception):
    """Исключение для ошибок во входных данных.
    Attributes:
        expression -- выражение, в котором произошла ошибка
        message -- объяснение ошибки, ответ пользователю
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


async def error_catched(update: types.Update, exception):
    if isinstance(exception, SearchError):
        logger.debug("User {0} SearchError: {1}".format(update.message.from_user.id, exception.expression))
        await update.message.answer(exception.message)

    elif isinstance(exception, MessageIsTooLong):
        await update.message.answer("Сообщение слишком длинное!")

    elif isinstance(exception, BotBlocked):
        logger.warning("User {0} blocked bot!".format(update.message.from_user.id))
        users.remove_user(str(update.message.from_user.id))
        reminders.remove(str(update.message.chat.id))
        logger.debug("User {0} removed from database.".format(update.message.from_user.id))

    elif isinstance(exception, CantParseEntities):
        logger.error("HTML tag is not close!\n\tException: {1}".format(update.message.from_user.id, exception))

    else:
        logger.error("Found exception with user {0}!\n\tException: {1}".format(update.message.from_user.id, exception))
        await update.message.answer("Возникла какая-то ошибка!")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True


def register_handlers_error(dp: Dispatcher):
    dp.register_errors_handler(error_catched)



