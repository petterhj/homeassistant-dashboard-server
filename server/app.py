from fastapi import FastAPI, Depends, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi_utils.tasks import repeat_every
from loguru import logger
from pydantic import ValidationError

from .dependencies import get_config, get_captures
from .logger import configure_logger
from .models.config import Config, CaptureFormat
from .models.server import ServerConfig
from .routers.api import router as api_router
from .routers.proxy import router as proxy_router
from .routers.static import (
    router as static_router,
    dashboard_static,
)
from .capture import capture_screenshot


server_config = ServerConfig()
configure_logger(server_config)

app = FastAPI()
app.include_router(api_router, prefix="/api")
app.include_router(proxy_router, prefix="/api/ha")
app.include_router(static_router)


@app.exception_handler(ValidationError)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(exc)

    errors = []
    for error in exc.errors(): 
        errors.append({
            "location": ".".join([str(l) for l in error["loc"] if l not in ["response"]]),
            "message": error["msg"],
        })

    return JSONResponse(
        content=jsonable_encoder({"detail": errors}),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@app.on_event("startup")
@repeat_every(
    seconds=server_config.capture_interval,
    wait_first=True,
    raise_exceptions=True,
)
async def capture_dashboard_task() -> None:
    config = get_config()
    target_url = f"http://localhost:{config.server.port}/"

    logger.info("Running capture task, url={}, {}".format(
        target_url,
        config.capture,
    ))

    await capture_screenshot(
        url=target_url,
        server_config=config.server,
        capture_config=config.capture,
        timezone=config.timezone,
        name="dashboard",
    )


@app.get("/dashboard.{capture_format}")
async def capture(
    capture_format: CaptureFormat,
    capture_files: list = Depends(get_captures),
):
    if len(capture_files) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No capture files found",
        )
    return FileResponse(
        capture_files[0],
        media_type=f"image/{capture_format.value}",
    )


@app.get("/{remote_id}.{capture_format}")
async def remote_capture(
    remote_id: str,
    capture_format: CaptureFormat,
):
    config = get_config()

    if not config.remote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No remotes configured",
        )

    if remote_id not in config.remote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unknown remote ID provided (valid: {})".format(
                ", ".join(f"`{id}`" for id in config.remote.keys()),
            ),
        )

    remote_config = config.remote[remote_id]
    capture_config = config.capture.copy(
        update=remote_config.capture.dict(exclude_defaults=True),
    ) if remote_config.capture else config.capture

    captured_file_path = await capture_screenshot(
        url=remote_config.url,
        server_config=config.server,
        capture_config=capture_config,
        timezone=config.timezone,
        name=remote_id,
    )

    return FileResponse(
        captured_file_path,
        media_type=f"image/{capture_format.value}",
    )


app.mount("/", dashboard_static(), name="dashboard")
