import asyncio
import json
import logging
import os

from playwright.async_api import (
    async_playwright,
    BrowserContext,
    TimeoutError,
)

from . import config


logger = logging.getLogger(__name__)

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
    logger.debug(f"Opening page, url={dashboard_url}")
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
        logger.warning("Page visit timed out!")
        return

    logger.info(f"Visited dashboard, title=\"{title}\"")

    await page.add_style_tag(content=dashboard_style)

    if config.SCREENSHOT_DELAY > 0:
        logger.debug(f"Sleeping {config.SCREENSHOT_DELAY} seconds")
        await asyncio.sleep(config.SCREENSHOT_DELAY)
    
    logger.info(f"Taking screenshot, target={config.SCREENSHOT_OUTPUT_PATH}")

    dirname = os.path.dirname(config.SCREENSHOT_OUTPUT_PATH)

    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)

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
    logger.debug("Page closed")


async def screenshot_task():
    async with async_playwright() as p:
        logger.info("Launching browser...")
        browser = await p.chromium.launch(
            headless=not config.DEBUG,
            slow_mo=1000 if config.DEBUG else 0,
        )
        context = await browser.new_context()

        logger.info("Adding authentication entry to browser's local storage...");
        page = await context.new_page();
        
        try:
            await page.goto(config.HA_BASE_URL, timeout=config.SCREENSHOT_TIMEOUT)
        except TimeoutError:
            logger.error("Timed out while authenticating")
            await page.close()
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
        logger.debug(f"Stored access token, type={json.loads(r)['token_type']}")

        await page.close()

        await take_screenshot(context)

        while True:
            logger.debug(f"Sleeping {config.SCREENSHOT_INTERVAL} seconds")
            await asyncio.sleep(config.SCREENSHOT_INTERVAL)
            await take_screenshot(context)
