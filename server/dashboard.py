from fastapi import APIRouter, Depends, HTTPException, Path, status
from yaml import safe_load

from .config import get_settings, Settings
# from .models import DashboardConfig


router = APIRouter(prefix="/config")


async def get_dashboard_config(
    settings: Settings = Depends(get_settings),
) -> dict:
    with open(settings.dashboard_config, "r") as config_file:
        return safe_load(config_file)


@router.get("/")
async def dashboard(
    config: dict = Depends(get_dashboard_config),
):
    return config
