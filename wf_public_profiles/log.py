import logging
from logging.config import dictConfig


from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "wf_public_profiles"
    LOG_FORMAT: str = "%(asctime)s,%(msecs)03d | %(levelprefix)s | %(name)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "access": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    }
    loggers = {
        "wf_public_profiles": {"handlers": ["default"], "level": LOG_LEVEL},
    }


class UvicornLogger(LogConfig):
    LOGGER_NAME: str = "wf_public_profiles.uvicorn"

    loggers = {
        "uvicorn.error": {"handlers": ["default"], "level": LogConfig().LOG_LEVEL, "propagate": "no"},
        "uvicorn.access": {"handlers": ["access"], "level": LogConfig().LOG_LEVEL, "propagate": "no"},
    }


dictConfig(LogConfig().dict())
logger = logging.getLogger("wf_public_profiles")
