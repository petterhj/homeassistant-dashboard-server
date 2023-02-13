from fastapi import APIRouter, Depends
from homeassistant_api import Client

from .config import get_settings, Settings


router = APIRouter()

async def get_client(
    settings: Settings = Depends(get_settings),
):
    yield Client(
        settings.homeassistant_host,
        settings.homeassistant_token,
    )


@router.get("/ha/entity")
async def entity(
    client: Client = Depends(get_client)
):
    sun = client.get_entity(entity_id="sun.sun")
    print(sun)
    return {}
