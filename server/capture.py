from asyncio import sleep
from pathlib import Path
from textwrap import wrap
from datetime import datetime

from fastapi import APIRouter
from loguru import logger
from PIL import Image, ImageFont, ImageDraw 
from playwright.async_api import (
    async_playwright,
    TimeoutError,
)

from .models.config import CaptureConfig, CaptureFormat
from .models.server import ServerConfig


assets_path = Path(__file__).parent.resolve() / "assets"
router = APIRouter()


async def capture_screenshot(
    url: str,
    server_config: ServerConfig,
    capture_config: CaptureConfig,
    timezone: str,
) -> None:
    capture_path = server_config.capture_path
    tmp_capture_file = capture_path / "capture_tmp.png"
    error_message = "Unknown error occured"
    
    args = {"device_scale_factor": capture_config.scale}

    if capture_config.width and capture_config.height:
        args["viewport"] = {
            "width": capture_config.width,
            "height": capture_config.height,
        }

    if timezone:
        args["timezone_id"] = timezone

    async with async_playwright() as p:
        try:
            logger.info(f"Launching browser, url=\"{url}\", args={args}")

            browser = await p.chromium.launch()
            context = await browser.new_context(**args)

        except Exception as e:
            logger.exception("Could not launch browser")
            error_message = str(e)

        else:
            try:
                logger.debug(f"Navigating to {url}")
                page = await context.new_page()

                await page.goto(
                    url=str(url),
                    wait_until="networkidle",
                    timeout=capture_config.timeout,
                )

                if capture_config.delay:
                    logger.debug(f"Delaying screenshot by {capture_config.delay} ms.")
                    await sleep(capture_config.delay / 1000)

                logger.info(f"Capturing screenshot (timeout={capture_config.timeout} ms.)")

                await page.screenshot(
                    path=tmp_capture_file,
                    timeout=capture_config.timeout,
                )

            except TimeoutError as e:
                logger.error(f"Timeout while generating screenshot: {e}")
                error_message = "Timeout"

            except Exception as e:
                logger.exception("Could not generate screenshot")
                error_message = str(e)

            finally:
                logger.debug("Closing the page")
                await page.close()

    logger.debug(f"Capture file exists: {tmp_capture_file.exists()}")

    if tmp_capture_file.exists():
        save_image(
            image=Image.open(tmp_capture_file),
            server_config=server_config,
            capture_config=capture_config,
        )

    else:
        save_image(
            image=generate_fallback_image(capture_config, error_message),
            server_config=server_config,
            capture_config=capture_config,
        )
    
    capture_cleanup(server_config)


def save_image(
    image: Image,
    server_config: ServerConfig,
    capture_config: CaptureConfig,
) -> None:
    output_format = capture_config.format
    bit_depth = capture_config.bit_depth

    logger.info(f"Saving image as {output_format.upper()}")

    output_file = server_config.capture_path / "capture_{}.{}".format(
        datetime.now().isoformat(timespec="seconds").replace(":", "."),
        output_format.value.lower(),
    )

    if output_format == CaptureFormat.png and bit_depth:
        logger.info(f"Converting image, bith_depth={bit_depth}")
        image = image.convert("P", palette=Image.ADAPTIVE, colors=bit_depth)

    image.save(output_file, output_format.value.upper())
    logger.debug(f"Saved image to {output_file}")
    

def generate_fallback_image(
    capture_config: CaptureConfig,
    message: str = None,
) -> Image:
    logger.info("Generating fallback image, width={}, height={}".format(
        capture_config.width,
        capture_config.height,
    ))

    fallback_path = assets_path / "static" / "error.png"
    font_path = assets_path / "jetbrains-mono.ttf"

    try:
        fallback_img = Image.open(fallback_path)
        target_size = fallback_img.size

        if capture_config.width and capture_config.height:
            target_size = (capture_config.width, capture_config.height)

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


def capture_cleanup(server_config: ServerConfig) -> None:
    logger.info("Cleaning up capture files")

    capture_path = server_config.capture_path
    capture_keep_count = server_config.capture_keep_count
    tmp_capture_file = capture_path / "capture_tmp.png"

    if not capture_path.exists():
        return

    if tmp_capture_file.exists():
        logger.debug(f"Deleting temporary capture file `{tmp_capture_file}`")
        tmp_capture_file.unlink()

    for capture_format in CaptureFormat:
        capture_files = sorted([
            f for f in capture_path.glob(f"*.{capture_format.value}")
        ])

        if len(capture_files) <= capture_keep_count:
            continue

        logger.info("Deleting {}/{} capture files of type {}".format(
            len(capture_files) - capture_keep_count,
            len(capture_files),
            capture_format.value,
        ))

        for file in capture_files[:-capture_keep_count]:
            logger.debug(f"Deleting capture file `{file}`")
            file.unlink()
