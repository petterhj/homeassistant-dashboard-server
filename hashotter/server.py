import logging

from aiohttp import web

from . import config

# logging.basicConfig(level=logging.DEBUG if config.DEBUG else logging.INFO)
logger = logging.getLogger(__name__)


class HttpServer(web.Application):
    def start(self, loop):
        self.add_routes([
            web.get(config.SERVER_OUTPUT_PATH, self.dashboard),
        ])

        handler = self.make_handler()
        server = loop.create_server(
            handler,
            host=config.SERVER_HOST,
            port=config.SERVER_PORT
        )

        logger.info("Serving output at http://{}:{}{}".format(
            config.SERVER_HOST, config.SERVER_PORT, config.SERVER_OUTPUT_PATH
        ))

        return server

    async def dashboard(self, request):
        return web.FileResponse(config.SCREENSHOT_OUTPUT_PATH)
