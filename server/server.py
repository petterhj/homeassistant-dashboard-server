import logging
import os
from pathlib import Path

from aiohttp import web

from . import config

# logging.basicConfig(level=logging.DEBUG if config.DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

static_dir_path = Path('dashboard/dist')

@web.middleware
async def static_serve(request, handler):
    print('-' * 50)
    relative_file_path = Path(request.path).relative_to('/')
    file_path = static_dir_path / relative_file_path
    print('> request.path=', request.path)
    print('> static_dir_path=', static_dir_path)
    print('> relative_file_path=', relative_file_path)
    print('> file_path=', file_path)
    print('> file_path.resolve=', file_path.resolve())
    print('> file_path.exists=', file_path.exists())
    print('-' * 50)
    if not file_path.exists():
        return web.HTTPNotFound()
    if file_path.is_dir():
        file_path = file_path / 'index.html'
        if not file_path.exists():
            return web.HTTPNotFound()
    return web.FileResponse(file_path)


class HttpServer(web.Application):
    def start(self, loop):
        # self.add_routes([
        #     web.get('/', self.dashboard),
        # ])
        # self.add_routes([
        #     web.get(config.SERVER_OUTPUT_PATH, self.screenshot),
        # ])

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

    """
    async def dashboard(self, request):
        static_dir_path = Path('dist')
        relative_file_path = Path(request.path).relative_to('/')  # remove root '/'
        file_path = static_dir_path / relative_file_path  # rebase into static dir
        print('static_dir_path', static_dir_path)
        print('relative_file_path', relative_file_path)
        print('file_path', file_path)
        if not file_path.exists():
            print("FILE NOT EXIST")
            return web.HTTPNotFound()
        if file_path.is_dir():
            file_path /= 'index.html'
            if not file_path.exists():
                return web.HTTPNotFound()
        return web.FileResponse(file_path)

    async def screenshot(self):
        if not os.path.exists(config.SCREENSHOT_OUTPUT_PATH):
            raise web.HTTPNotFound()
        return web.FileResponse(config.SCREENSHOT_OUTPUT_PATH)
    """

app = HttpServer(middlewares=[static_serve])
