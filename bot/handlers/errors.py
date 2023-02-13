import logging

from config.config_reader import load_config

from aiogram import Dispatcher, types
# from aiogram.utils.exceptions import BotBlocked


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


async def error_bot_blocked(update: types.Update, exception):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    # logger.error("User {0} blocked me!\n\tException: {1}".format(update.message.from_user.id, exception))
    logger.error("Found exception with user {0}!!!\n\tException: {1}".format(update.message.from_user.id, exception))

    # обработка конкретной ошибки
    # if isinstance(exception, BotBlocked):
    #     pass

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True

def register_handlers_error(dp: Dispatcher):
    dp.register_errors_handler(error_bot_blocked)



