from asyncio import sleep
from io import BytesIO
from pathlib import Path
from textwrap import wrap

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import (
    FileResponse,
    JSONResponse,
    StreamingResponse,
)
from fastapi.staticfiles import StaticFiles
from loguru import logger
from PIL import Image, ImageFont, ImageDraw 
from playwright.async_api import (
    async_playwright,
    TimeoutError,
)
from starlette.background import BackgroundTask

from .dependencies import get_config
from .models.config import Config
from .models.server import ScreenshotConfig, OutputFormat
from .routers.static import templates


assets_path = Path(__file__).parent.resolve() / "assets"
router = APIRouter()


def cleanup_task(path: str) -> None:
    logger.info(f"Deleting screenshot file `{path}`")
    path.unlink()


async def take_screenshot(
    url: str,
    config: ScreenshotConfig,
    format: OutputFormat,
) -> FileResponse:
    output_path = Path.cwd() / "capture.png"
    error_message = None
    
    args = {"device_scale_factor": config.scale}

    if config.width and config.height:
        args["viewport"] = {"width": config.width, "height": config.height}

    print(args)

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

            if config.delay:
                logger.debug(f"Delaying screenshot by {config.delay} ms.")
                await sleep(config.delay / 1000)

            logger.info(f"Capturing screenshot (timeout={config.timeout} ms.)")

            await page.screenshot(path=output_path, timeout=config.timeout)

        except TimeoutError as e:
            logger.error(f"Timeout while generating screenshot: {e}")
            error_message = "Timeout"

        except Exception as e:
            logger.exception("Could not generate screenshot")
            error_message = str(e)

        finally:
            await page.close()

    if not output_path.exists():
        return generate_fallback_image(config, error_message)

    response = FileResponse(output_path)
    response.background = BackgroundTask(cleanup_task, output_path)
    return response


def generate_fallback_image(
    config: ScreenshotConfig,
    message: str = None,
) -> FileResponse:
    logger.info("Generating fallback image")

    fallback_path = assets_path / "static" / "error.png"
    font_path = assets_path / "jetbrains-mono.ttf"
    response = FileResponse(fallback_path)

    try:
        fallback_img = Image.open(fallback_path)
        output_img = BytesIO()
        target_size = fallback_img.size

        if config.width and config.height:
            target_size = (config.width, config.height)

        fallback_img.thumbnail(target_size, Image.LANCZOS)
        new_img = Image.new("RGB", target_size, (255, 255, 255))
        new_img.paste(fallback_img, (
            int((target_size[0] - fallback_img.size[0]) / 2),
            int((target_size[1] - fallback_img.size[1]) / 2)
        ))

        if message:
            font = ImageFont.truetype(str(font_path), 20)
            draw = ImageDraw.Draw(new_img)
            draw.text(
                (15, 15),
                "\n".join(wrap(message, 50)),
                font=font,
                stroke_width=2,
                stroke_fill=(255, 255, 255),
                fill=(0, 0, 0),
            )

        new_img.save(output_img, "PNG")
        output_img.seek(0)

        return StreamingResponse(content=output_img, media_type="image/png")

    except Exception:
        logger.exception("Could not generate fallback image")

    return response
