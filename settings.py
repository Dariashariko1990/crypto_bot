
BOT_API_TOKEN = ''
BOT_STORAGE = None

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {},
    "formatters": {
        "standard": {"format": "[%(asctime)s] [%(levelname)s %(name)s] %(message)s"},
        "simple": {"format": "[%(name)s] %(asctime)s %(message)s"},
    },
    "handlers": {
        "stream": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {
            "handlers": ["stream"],
            "level": "DEBUG",
        },
    },
}
