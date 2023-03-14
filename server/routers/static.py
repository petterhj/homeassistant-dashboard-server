from pathlib import Path

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

from ..dependencies import get_config


assets_path = Path(__file__).parent.parent.resolve() / "assets"
router = APIRouter()
templates = Jinja2Templates(directory=f"{assets_path.resolve()}/templates")


def dashboard_static():
    try:
        config = get_config()
    except ValidationError as e:
        return templates.TemplateResponse("dashboard/error.html", {
            "request": {},
            "message": f"Invalid configuration",
        })

    static_path = config.server.static_path.resolve()
    
    if not static_path.exists():
        return templates.TemplateResponse("dashboard/error.html", {
            "request": {},
            "message": f"Static path `{static_path}` not found.",
        })

    return StaticFiles(directory=static_path, html=True)


@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(assets_path / "static" / "favicon.ico")


@router.get('/error.bmp', include_in_schema=False)
async def error():
    return FileResponse(assets_path / "static" / "error.bmp")
