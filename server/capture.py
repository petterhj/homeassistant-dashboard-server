from datetime import datetime
from pathlib import Path
from textwrap import wrap
from time import mktime

from fastapi import APIRouter
from loguru import logger
from PIL import Image, ImageFont, ImageDraw, ImageOps
from playwright.async_api import (
    async_playwright,
    TimeoutError,
)

from .models.config import Config, CaptureConfig, CaptureFormat
from .models.server import ServerConfig


assets_path = Path(__file__).parent.resolve() / "assets"
router = APIRouter()


async def capture_screenshot(
    config: Config,
    url: str,
    view_name: str,
) -> Path:
    capture_path = config.server.capture_path
    tmp_capture_file = capture_path / "capture_tmp.png"
    error_message = "Unknown error occured"

    args = {"device_scale_factor": config.capture.scale}

    if config.capture.width and config.capture.height:
        args["viewport"] = {
            "width": config.capture.width,
            "height": config.capture.height,
        }

    if config.timezone:
        args["timezone_id"] = config.timezone

    args["locale"] = "no-NO" if config.locale == "nb" else "en-GB"

    async with async_playwright() as p:
        try:
            logger.info(f'Launching browser, url="{url}", args={args}')
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
                    wait_until=config.capture.wait_until,
                    timeout=config.capture.timeout,
                )

                if config.capture.delay:
                    logger.info(
                        f"Delaying screenshot by {config.capture.delay} ms."
                    )
                    await page.wait_for_timeout(config.capture.delay)

                logger.info(
                    "Capturing screenshot (view={}, timeout={} ms.)".format(
                        view_name,
                        config.capture.timeout,
                    )
                )

                await page.screenshot(
                    path=tmp_capture_file, timeout=config.capture.timeout
                )

            except TimeoutError as e:
                logger.error(f"Timeout while generating screenshot: {e}")
                error_message = f"Timeout ({config.capture.timeout} ms.)"

            except Exception as e:
                logger.exception("Could not generate screenshot")
                error_message = str(e)

            finally:
                logger.debug("Closing the page")
                await page.close()

    logger.debug(f"Capture file exists: {tmp_capture_file.exists()}")
    captured_file_path = None

    if tmp_capture_file.exists():
        captured_file_path = save_image(
            image=Image.open(tmp_capture_file),
            server_config=config.server,
            capture_config=config.capture,
            name=view_name,
        )

    else:
        captured_file_path = save_image(
            image=generate_fallback_image(config.capture, error_message),
            server_config=config.server,
            capture_config=config.capture,
            name=view_name,
        )

    capture_cleanup(config.server)
    return captured_file_path


def save_image(
    image: Image,
    server_config: ServerConfig,
    capture_config: CaptureConfig,
    name: str,
) -> Path:
    output_format = capture_config.format
    output_file = server_config.capture_path / "{}_{}.{}".format(
        int(mktime(datetime.now().timetuple())),
        name,
        output_format.value.lower(),
    )

    # Invert
    if capture_config.invert:
        if image.mode in ("L", "P"):
            image = ImageOps.invert(image)
        else:
            image = image.convert("RGB")
            image = ImageOps.invert(image)

    # Grayscale
    if capture_config.grayscale and image.mode != "L":
        image = image.convert("L")

    # Resize (if needed)
    if capture_config.width and capture_config.height:
        if image.size != (capture_config.width, capture_config.height):
            image = image.resize(
                (capture_config.width, capture_config.height), Image.LANCZOS
            )

    try:
        image.save(output_file, output_format.value.upper())
    except Exception as e:
        logger.error(f"Failed to save image: {e}")
        image.save(output_file)

    return output_file


def generate_fallback_image(
    capture_config: CaptureConfig = CaptureConfig(),
    message: str = None,
) -> Image:
    logger.info(
        "Generating fallback image, width={}, height={}, message={}".format(
            capture_config.width,
            capture_config.height,
            message,
        )
    )

    fallback_path = assets_path / "static" / "error.png"
    font_path = assets_path / "jetbrains-mono.ttf"

    try:
        fallback_img = Image.open(fallback_path)
        target_size = fallback_img.size

        if capture_config.width and capture_config.height:
            target_size = (capture_config.width, capture_config.height)

        fallback_img.thumbnail(target_size, Image.LANCZOS)
        new_img = Image.new("RGB", target_size, (255, 255, 255))
        new_img.paste(
            fallback_img,
            (
                int((target_size[0] - fallback_img.size[0]) / 2),
                int((target_size[1] - fallback_img.size[1]) / 2),
            ),
        )

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
        capture_files = sorted(
            [f for f in capture_path.glob(f"*.{capture_format.value}")]
        )

        if len(capture_files) <= capture_keep_count:
            continue

        logger.info(
            "Deleting {}/{} capture files of type {}".format(
                len(capture_files) - capture_keep_count,
                len(capture_files),
                capture_format.value,
            )
        )

        for file in capture_files[:-capture_keep_count]:
            logger.debug(f"Deleting capture file `{file}`")
            file.unlink()
