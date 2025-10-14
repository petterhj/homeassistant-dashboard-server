from fastapi import APIRouter, Depends, status, HTTPException

from ..dependencies import get_config, get_view, get_views
from ..models.capture import Capture, CaptureDetails, CaptureFormat
from ..models.config import Config
from ..models.view import View
from ..util import get_image_details


router = APIRouter()


@router.get("   ")
@router.get("/config")
async def config(
    config: dict = Depends(get_config),
) -> Config:
    return config


@router.get("/views", summary="List all views")
async def list_views(
    views: list = Depends(get_views),
) -> list[View]:
    return views


@router.get("/views/{view_name}", summary="Get view details")
async def view_details(view: View = Depends(get_view)) -> View:
    return view


@router.get(
    "/captures",
    name="list_all_captures",
    summary="List all capture files",
)
@router.get(
    "/views/{view_name}/captures",
    name="list_view_captures",
    summary="List captures for a view",
)
async def list_captures(
    view_name: str = None,
    capture_format: CaptureFormat = None,
    views: list = Depends(get_views),
) -> list[Capture]:
    if view_name and view_name not in [view.name for view in views]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"View '{view_name}' not found",
        )

    captures = []

    for view in views:
        if view_name and view.name != view_name:
            continue
        captures.extend(view.captures)

    captures = sorted(captures, key=lambda c: c.timestamp, reverse=True)

    if capture_format:
        captures = [c for c in captures if c.format == capture_format]

    return captures


@router.get("/captures/{filename:str}", summary="Get capture details")
@router.get(
    "/views/{view_name}/captures/last",
    summary="Get capture details for last view capture",
)
async def get_capture(
    filename: str = None,
    view_name: str = None,
    views: list = Depends(get_views),
    config: Config = Depends(get_config),
) -> CaptureDetails:
    if view_name and view_name not in [view.name for view in views]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"View '{view_name}' not found",
        )

    if view_name and not filename:
        view = next((v for v in views if v.name == view_name), None)
        if view and view.last_capture:
            return CaptureDetails(
                **view.last_capture.model_dump(),
                **get_image_details(
                    config.server.capture_path / view.last_capture.filename
                ),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No captures found for view",
            )

    for view in views:
        if capture := next(
            (c for c in view.captures if c.filename == filename), None
        ):
            return CaptureDetails(
                **capture.model_dump(),
                **get_image_details(
                    config.server.capture_path / capture.filename
                ),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No captures found for view",
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Capture not found"
    )
