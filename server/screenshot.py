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
from .models.server import ScreenshotConfig, ServerConfig, OutputFormat
from .routers.static import templates


assets_path = Path(__file__).parent.resolve() / "assets"
router = APIRouter()


def cleanup_task(path: str) -> None:
    logger.info(f"Deleting screenshot file `{path}`")
    path.unlink()


async def take_screenshot(
    url: str,
    server_config: ServerConfig,
    screenshot_config: ScreenshotConfig,
    output_format: OutputFormat,
) -> FileResponse:
    output_path = server_config.data_path / "capture.png"
    error_message = None
    
    args = {"device_scale_factor": screenshot_config.scale}

    if screenshot_config.width and screenshot_config.height:
        args["viewport"] = {
            "width": screenshot_config.width,
            "height": screenshot_config.height,
        }

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
                timeout=screenshot_config.timeout,
            )

            if screenshot_config.delay:
                logger.debug(f"Delaying screenshot by {screenshot_config.delay} ms.")
                await sleep(screenshot_config.delay / 1000)

            logger.info(f"Capturing screenshot (timeout={screenshot_config.timeout} ms.)")

            await page.screenshot(path=output_path, timeout=screenshot_config.timeout)

        except TimeoutError as e:
            logger.error(f"Timeout while generating screenshot: {e}")
            error_message = "Timeout"

        except Exception as e:
            logger.exception("Could not generate screenshot")
            error_message = str(e)

        finally:
            await page.close()

    if output_path.exists():
        output_stream = convert_image(
            image=Image.open(output_path),
            screenshot_config=screenshot_config,
            output_format=output_format,
        )
    else:
        output_stream = convert_image(
            image=generate_fallback_image(screenshot_config, error_message),
            screenshot_config=screenshot_config,
            output_format=output_format,
        )
    
    output_stream.seek(0)
    response = StreamingResponse(
        content=output_stream,
        media_type=f"image/{output_format.value}",
    )
    response.background = BackgroundTask(cleanup_task, output_path)
    return response


def convert_image(
    image: Image,
    screenshot_config: ScreenshotConfig,
    output_format: OutputFormat,
) -> BytesIO:
    output_format = output_format.value.upper()
    logger.info(f"Saving image as {output_format}")
    output_img = BytesIO()
    image.save(output_img, output_format)
    return output_img


def generate_fallback_image(
    screenshot_config: ScreenshotConfig,
    message: str = None,
) -> Image:
    logger.info("Generating fallback image")

    fallback_path = assets_path / "static" / "error.png"
    font_path = assets_path / "jetbrains-mono.ttf"

    try:
        fallback_img = Image.open(fallback_path)
        target_size = fallback_img.size

        if screenshot_config.width and screenshot_config.height:
            target_size = (screenshot_config.width, screenshot_config.height)

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
    except Exception:
        logger.exception("Could not generate fallback image")
        raise
    return new_img
