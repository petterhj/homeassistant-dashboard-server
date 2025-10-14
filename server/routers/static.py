from pathlib import Path

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse


assets_path = Path(__file__).parent.parent.resolve() / "assets"
router = APIRouter()
templates = Jinja2Templates(directory=f"{assets_path.resolve()}/templates")


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(assets_path / "static" / "favicon.ico")


@router.get("/error.png", include_in_schema=False)
async def error():
    return FileResponse(assets_path / "static" / "error.png")
