import logging

import uvicorn

from .config import get_settings

settings = get_settings()

logging_level = logging.getLevelName(settings.log_level)
logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("-" * 25)
    logger.info(f"Host: {settings.host}")
    logger.info(f"Port: {settings.port}")
    logger.info(f"Debug: {settings.debug}")
    logger.info(f"Logging: {settings.log_level}")
    logger.info("-" * 25)

    uvicorn.run(
        'server.main:app',
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        reload_dirs=["./server/"],
        log_level=logging_level,
    )
