import logging
from logging.config import dictConfig
from tabnanny import verbose

# token
DISCORD_TOKEN =(
"MTIyMzI2NzIyNjcxOTc0ODE5Nw.GkMoZ6.rU14H6Bqv3szbk5P8pbOpu5sDxdZJusQbJeOxI"
)

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
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose"
        }
    },
    "loggers":{
        "bot": {
            "handlers": ["console"],
            "level": "INFO",
            "propogate": False
        },
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propogate": False
        }
    }
}

dictConfig(LOGGING_CONFIG)

# owner ids
owner_ids = [575555247557312512, 1195470182831894558, 1092184838225809458]