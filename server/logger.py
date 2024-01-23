import logging
import sys

from loguru import logger

from .models.server import ServerConfig


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def configure_logger(config: ServerConfig):
    # log_level = logging.getLevelName(config.log_level.value.upper())

    # Intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    # logging.root.setLevel(logging.INFO)

    # Clear every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers.clear()
        logging.getLogger(name).propagate = True

    # Configure loguru
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "serialize": config.log_json,
                "level": config.log_level.value.upper(),
            },
            {
                "sink": config.data_path / config.log_filename,
                "rotation": "10 MB",
                "retention": "7 days",
                "serialize": config.log_json,
                "level": config.log_level.value.upper(),
            },
        ]
    )
