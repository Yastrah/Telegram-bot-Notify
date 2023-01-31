import configparser
from dataclasses import dataclass
import sys
import logging


logger = logging.getLogger(__name__)


@dataclass
class Bot:
    name: str
    id: str
    token: str
    admin_id: list


# @dataclass
# class Logger:
#     level: str
#     date_format: str


@dataclass
class Data:
    bot_db: str


@dataclass
class Config:
    bot: Bot
    # logger: Logger
    data: Data


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    try:
        bot_conf = config["bot"]
        # logger_conf = config["logger"]
        data_conf = config["data"]

        return Config(
            bot=Bot(
                name=bot_conf["name"],
                id=bot_conf["id"],
                token=bot_conf["token"],
                admin_id=bot_conf["admin_id"].split(),
            ),
            # logger=Logger(
            #     level=logger_conf["level"],
            #     date_format=logger_conf["date_format"].replace('&', '%'),
            # ),
            data=Data(
                bot_db=data_conf["bot_db"],
            )
        )
    except Exception as e:
        logger.error("Failed to load config file!\n\tException: {0}".format(e))
        sys.exit()