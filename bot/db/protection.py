import logging
import datetime

from bot.db import reminders, users
from bot.logic.date_converter import date_to_value
from config.configuration import Settings


logger = logging.getLogger(__name__)


def checking_for_old_reminders():
    data = reminders.read()
    now_date_value = date_to_value(datetime.datetime.now().strftime(Settings.date_format))

    if data is None:
        return logger.error("Unable to read and check database!")

    if not data:
        return logger.debug("Checking old reminders completed successfully. There is no any reminders.")

    count = 0
    for reminder in data:
        if date_to_value(reminder[4]) < now_date_value:
            reminders.remove(id=reminder[0])
            count += 1
    logger.debug("Checking old reminders completed successfully. Found {0} old reminders.".format(count))

