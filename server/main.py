from asyncio import sleep
from logging import getLogger
from pathlib import Path

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from playwright.async_api import (
    async_playwright,
    TimeoutError,
)

from .config import get_settings, Settings
from .proxy import router as proxy


logger = getLogger(__name__)
settings = get_settings()

app = FastAPI()
app.include_router(proxy)

def cleanup(path: str) -> None:
    logger.info(f"Deleting dashboard image {path}")
    path.unlink()


@app.get("/dashboard.png", response_class=FileResponse)
async def dashboard(
    request: Request,
    background_tasks: BackgroundTasks,
    settings: Settings = Depends(get_settings),
):
    output_path = Path(settings.screenshot_path)

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

app.mount(
    "/",
    StaticFiles(
        directory=settings.static_path
        if settings.static_path.exists()
        else settings.static_fallback_path,
        html=True,
    ),
    name="frontend",
)
