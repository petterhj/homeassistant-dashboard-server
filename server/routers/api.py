from pathlib import Path

from fastapi import APIRouter, Depends

from ..dependencies import get_config, get_captures
from ..models.config import Config


router = APIRouter()


@router.get("/config")
async def config(
    config: dict = Depends(get_config),
) -> Config:
    return config


@router.get("/captures/{capture_format}")
async def captures(
    capture_files: list = Depends(get_captures),
)  -> list[Path]:
    return capture_files
