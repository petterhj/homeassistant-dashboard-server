from asyncio import sleep
from pathlib import Path

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from playwright.async_api import (
    async_playwright,
    TimeoutError,
)
from starlette.background import BackgroundTask

from .dependencies import get_config
from .models.config import Config
from .models.server import ScreenshotConfig
from .routers.static import templates


router = APIRouter()



def cleanup_task(path: str) -> None:
    logger.info(f"Deleting screenshot file `{path}`")
    path.unlink()


async def take_screenshot(url, config: ScreenshotConfig) -> FileResponse:
    output_path = Path.cwd() / "capture.png"
    fallback_path = Path(__file__).parent.resolve() / "assets" / "static" / "error.bmp"
    
    args = {"device_scale_factor": config.scale}

    if config.width and config.height:
        args["viewport"] = {"width": config.width, "height": config.height}
        
    async with async_playwright() as p:
        logger.info(f"Launching browser, url=\"{url}\", args={args}")
        browser = await p.chromium.launch()
        context = await browser.new_context(**args)

        try:
            logger.debug(f"Navigating to {url}")
            page = await context.new_page()
            await page.goto(
                url=str(url),
                wait_until="networkidle",
                timeout=config.timeout,
            )

            if config.delay > 0:
                logger.debug(f"Delaying screenshot by {config.delay} ms.")
                await sleep(config.delay / 1000)

            logger.info(f"Capturing screenshot (timeout={config.timeout} ms.)")

            await page.screenshot(path=output_path, timeout=config.timeout)

        except TimeoutError as e:
            logger.error(f"Could not generate screenshot: {e}")

        finally:
            await page.close()

    if output_path.exists():
        response = FileResponse(output_path)
        response.background = BackgroundTask(cleanup_task, output_path)
    else:
        response = FileResponse(fallback_path)

    return response


'''
@router.get("/dashboard.png", response_class=FileResponse)
async def dashboard(
    request: Request,
    background_tasks: BackgroundTasks,
    config: Config = Depends(get_config),
):
    print(config)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Dashboard screenshot nor fallback image found",
    )
    # output_path = Path(settings.screenshot_path)

    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            device_scale_factor=settings.screenshot_scaling,
            viewport={
                "width": settings.screenshot_width,
                "height": settings.screenshot_height,
            },
        )

        try:
            page = await context.new_page()
            await page.goto(
                url=str(request.base_url),
                wait_until="networkidle",
                timeout=settings.screenshot_timeout,
            )

            if settings.screenshot_delay:
                logger.info(f"Delaying screenshot by {settings.screenshot_delay} ms.")
                await sleep(settings.screenshot_delay / 1000)

            logger.info(f"Capturing screenshot (timeout={settings.screenshot_timeout} ms.)")
            await page.screenshot(
                path=output_path,
                timeout=settings.screenshot_timeout,
            )
        except TimeoutError as e:
            logger.error(f"Could not generate screenshot: {e}")
        finally:
            await page.close()

    if output_path.exists():
        background_tasks.add_task(cleanup, output_path)
    else:
        fallback_image = settings.static_fallback_path / "fallback.jpg"
        if fallback_image.exists():
            output_path = fallback_image
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dashboard screenshot nor fallback image found",
            )
    return FileResponse(output_path)
    """
'''