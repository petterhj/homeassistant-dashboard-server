from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from starlette.responses import Response
from loguru import logger
from pydantic import ValidationError

from .dependencies import get_config, get_view
from .logger import configure_logger
from .models.capture import CaptureFormat
from .models.config import Config
from .models.server import ServerConfig
from .models.view import View
from .routers.api import router as api_router
from .routers.proxy import router as proxy_router
from .routers.static import router as static_router, templates
from .exceptions import ConfigurationError
from .capture import capture_screenshot
from .util import repeat_every


server_config = ServerConfig()
configure_logger(server_config)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await capture_task()
    yield


app = FastAPI(
    lifespan=lifespan,
    redirect_slashes=False,
)

app.include_router(api_router, prefix="/api")
app.include_router(proxy_router, prefix="/api/ha")
app.include_router(static_router)


@app.exception_handler(ConfigurationError)
@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def exception_handler(request: Request, exc: Exception) -> Response:
    logger.error(
        f"{type(exc).__name__} when requesting {request.url.path}: {exc}"
    )
    is_api_request = request.url.path.startswith("/api/")

    if not is_api_request:
        return templates.TemplateResponse(
            "dashboard/error.html",
            {
                "request": request,
                "message": "Configuration Error",
                "details": str(exc),
            },
        )

    # Handle validation errors (ValidationError, RequestValidationError)
    if isinstance(exc, (ValidationError, RequestValidationError)):
        errors = []
        for error in exc.errors():
            errors.append(
                {
                    "location": ".".join(
                        [str(l) for l in error["loc"] if l not in ["response"]]
                    ),
                    "message": error["msg"],
                }
            )

        return JSONResponse(
            content=jsonable_encoder({"detail": errors}),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    # Handle configuration errors
    elif isinstance(exc, ConfigurationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Configuration Error",
                "message": str(exc),
            },
        )


@repeat_every(
    seconds=server_config.capture_interval,
    wait_first=server_config.capture_wait_first,
    raise_exceptions=True,
)
async def capture_task() -> None:
    try:
        config = get_config()
        views = {view.name: view for view in config.views}
    except (ValidationError, ConfigurationError) as e:
        logger.error(f"Skipping capture: Invalid configuration: {e}")
        return

    views_to_capture = config.server.capture_views or [
        view.name for view in views.values()
    ]

    logger.info(
        f"Running capture task for views: {', '.join(views_to_capture)}"
    )

    for view in views_to_capture:
        if view not in views:
            logger.warning(
                f"Skipping capture: Capture view '{view}' not configured"
            )
            continue

        view = views[view]
        target_url = f"http://localhost:{config.server.port}/{view.name}"
        logger.info(f"Capturing view '{view.name}' from {target_url}")
        await capture_screenshot(
            config=config, url=target_url, view_name=view.name
        )


@app.get("/{view_name:str}.{capture_format:str}", summary="Show capture")
@app.get("/{timestamp:int}_{view_name:str}.{capture_format:str}", summary="Show historic capture")
async def show_capture(
    capture_format: CaptureFormat,
    timestamp: int = None,
    view: View = Depends(get_view),
    config: Config = Depends(get_config),
) -> FileResponse:
    capture = None

    if view.captures:
        if timestamp and (capture := next(
            (c for c in view.captures if c.timestamp == timestamp), None
        )):
            capture = capture
        else:
            capture = view.last_capture

        if capture and capture.format == capture_format:
            return FileResponse(
                config.server.capture_path / capture.filename,
                media_type=f"image/{capture_format.value}",
                headers={"Content-Disposition": "inline"}
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Capture not found for view '{view.name}'",
    )


# SPA handler - serves static files and Vue app
@app.get("/{path:path}", include_in_schema=False)
async def spa_handler(
    config: dict = Depends(get_config),
    path: str = "",
) -> FileResponse:
    static_path = config.server.static_path.resolve()

    # Handle root path
    if not path:
        path = "index.html"

    # Try to serve the actual file first (for JS, CSS, images, etc.)
    requested_file = static_path / path
    if requested_file.exists() and requested_file.is_file():
        return FileResponse(requested_file)

    # For Vue Router paths that don't correspond to files, serve index.html
    index_file = static_path / "index.html"
    if index_file.exists():
        return FileResponse(index_file, media_type="text/html")

    raise HTTPException(status_code=404, detail="Vue app not found")
