from pathlib import Path

from fastapi import APIRouter, Depends, Request

from ..dependencies import get_config, get_captures
from ..models.config import Config, CaptureFormat


router = APIRouter()


@router.get("/config")
async def config(
    config: dict = Depends(get_config),
) -> Config:
    return config


@router.get("/captures/{capture_name}/{capture_format}")
async def captures(
    request: Request,
    capture_format: CaptureFormat,
    capture_files: list = Depends(get_captures),
) -> list[str]:
    return [
        str(
            request.url_for(
                "capture",
                capture_format=capture_format.value,
                timestamp=int(cf.name.split("_")[0]),
            )
        )
        for cf in capture_files
    ]
