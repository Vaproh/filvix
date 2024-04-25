import logging
from logging.config import dictConfig
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")

# token
DISCORD_TOKEN =os.getenv(
"DISCORD_TOKEN"
)

# Lavalink
lavalink_url = os.getenv("LAVALINK_URI")
lavalink_password = os.getenv("LAVALINK_PASSWORD")

# logger dict and func
LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s - %(name)-15s : %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "console3": {
            "level": "DEBUG",  # Change the level to a standard logging level
            "class": "logging.StreamHandler",
            "formatter": "standard"  
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose"
        },
        "file2": {
            "level": "DEBUG",  # Change the level to a standard logging level
            "class": "logging.FileHandler",
            "filename": "logs/lavalink.log",
            "mode": "w",
            "formatter": "verbose"
        },
    },
    "loggers": {
        "bot": {
            "handlers": ["console"],
            "level": "INFO",
            "propogate": False
        },
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propogate": False
        },
        "lavalink": {
            "handlers": ["console3", "file2"],
            "level": "DEBUG",  # Change the level to a standard logging level
            "propogate": False
        }
    }
}

dictConfig(LOGGING_CONFIG)

# owner ids
owner_ids = [575555247557312512, 1195470182831894558, 1092184838225809458]

# colors
color_main = 0x2D3250 # main color
color_sec = 0x424769 # secondary color
color_err = 0x7077A1 # error color

# text
footer_text = "is filvix bot is best right? - 2024"

# jishaku envirment variables
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"