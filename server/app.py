from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

from .dependencies import get_config
from .logger import configure_logger
from .models.config import Config
from .models.server import ServerConfig, ScreenshotConfig
from .routers.proxy import router as proxy_router
from .routers.static import (
    router as static_router,
    dashboard_static,
)
from .screenshot import take_screenshot


configure_logger(ServerConfig())

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Load the ML model
#     print("!" * 100)
#     # foo
#     yield
#     # Clean up the ML models and release the resources
#     print("?" * 100)
    

app = FastAPI()#lifespan=lifespan)
app.include_router(proxy_router, prefix="/ha")
app.include_router(static_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors(): 
        errors.append({
            "location": ".".join(list(error["loc"])),
            "message": error["msg"],
        })

    return JSONResponse(
        content=jsonable_encoder({"detail": errors}),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@app.middleware("http")
async def output_middleware(request: Request, call_next):
    if request.query_params.get("output") == "png":
        config = ScreenshotConfig.parse_obj(request.query_params)

        logger.info(f"Generating png out, config={config}")

        return await take_screenshot(
            url=request.url.remove_query_params(
                ["output", *config.__fields__.keys()]
            ),
            config=config,
        )
        
    return await call_next(request)


@app.get("/config")
async def config(
    config: dict = Depends(get_config),
) -> Config:
    return config


app.mount("/", dashboard_static(), name="dashboard")
