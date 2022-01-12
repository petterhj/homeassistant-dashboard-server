import asyncio
import logging

from hashotter.server import HttpServer
from hashotter.tasks import screenshot_task


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info("Starting...")
    loop = asyncio.get_event_loop()
    http_server = HttpServer()
    asyncio.ensure_future(http_server.start(loop), loop=loop)
    loop.create_task(screenshot_task())
    loop.run_forever()
