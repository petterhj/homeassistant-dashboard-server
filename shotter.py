import asyncio
import io
import json

from aiohttp import web
from playwright.async_api import (
    async_playwright,
    BrowserContext,
    TimeoutError,
)

import config


hass_tokens = {
    "hassUrl": config.HA_BASE_URL,
    "access_token": config.HA_ACCESS_TOKEN,
    "token_type": "Bearer",
}
dashboard_url = f"{config.HA_BASE_URL}{config.HA_DASHBOARD_URL}"
dashboard_style = (
    "body {"
    f"   width: calc({config.SCREENSHOT_WIDTH}px / {config.SCREENSHOT_SCALING});"
    f"   height: calc({config.SCREENSHOT_HEIGHT}px / {config.SCREENSHOT_SCALING});"
    "    transform-origin: 0 0;"
    f"   transform: scale({config.SCREENSHOT_SCALING});"
    "    overflow: hidden;"
    "}"
)


async def take_screenshot(context: BrowserContext):
    print(f"Opening page, url={dashboard_url}")
    page = await context.new_page()
    
    await page.emulate_media(color_scheme="light")
    await page.set_viewport_size(viewport_size={
        "width": config.SCREENSHOT_WIDTH,
        "height": config.SCREENSHOT_HEIGHT
    });

    try:
        await page.goto(
            url=dashboard_url,
            wait_until="load",
            timeout=config.SCREENSHOT_TIMEOUT,
        )
        title = await page.title()
    except TimeoutError:
        print("Page visit timed out!")
        return

    print(f"Visited page, title={title}")

    await page.add_style_tag(content=dashboard_style)

    if config.SCREENSHOT_DELAY > 0:
        print(f"Sleeping {config.SCREENSHOT_DELAY} seconds")
        await asyncio.sleep(config.SCREENSHOT_DELAY)
    
    await page.screenshot(
        path=config.SCREENSHOT_OUTPUT_PATH,
        clip={
            "x": 0,
            "y": 0,
            "width": config.SCREENSHOT_WIDTH,
            "height": config.SCREENSHOT_HEIGHT,
        },
        timeout=config.SCREENSHOT_TIMEOUT,
    )
    
    await page.close()


async def screenshot_task():
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.firefox.launch(
            headless=not config.DEBUG,
            # slow_mo=1000 if config.DEBUG else 0,
        )
        context = await browser.new_context()

        print("Adding authentication entry to browser's local storage...");
        page = await context.new_page();
        
        try:
            await page.goto(config.HA_BASE_URL, timeout=config.SCREENSHOT_TIMEOUT)
        except TimeoutError:
            return

        r = await page.evaluate(
            expression=(
                "(tokens) => {"
                "  localStorage.setItem('hassTokens', tokens);"
                "  return localStorage.getItem('hassTokens');"
                "}"
            ),
            arg=json.dumps(hass_tokens),
        )
        print(f"Stored access token, type={json.loads(r)['token_type']}")

        await page.close()

        await take_screenshot(context)

        if config.DEBUG:
            return

        while True:
            await asyncio.sleep(config.SCREENSHOT_INTERVAL)
            await take_screenshot(context)


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


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

        print(f"Hosting at {config.SERVER_HOST}:{config.SERVER_PORT}")

        return server

    async def dashboard(self, request):
        return web.FileResponse(config.SCREENSHOT_OUTPUT_PATH)


def main():
    loop = asyncio.get_event_loop()
    http_server = HttpServer()
    asyncio.ensure_future(http_server.start(loop), loop=loop)
    loop.create_task(screenshot_task())
    loop.run_forever()


if __name__ == '__main__':
    main()
