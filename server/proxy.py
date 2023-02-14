from fastapi import APIRouter, Depends, Path
from homeassistant_api import Client

from .config import get_settings, Settings


router = APIRouter()

async def get_client(
    settings: Settings = Depends(get_settings),
):
    yield Client(
        settings.homeassistant_host,
        settings.homeassistant_token.get_secret_value(),
    )


@router.get("/ha/entity/{entity_id}")
async def entity(
    client: Client = Depends(get_client),
    entity_id: str = Path(regex=r"^[0-9A-Za-z\_]+\.[0-9A-Za-z\_]+$")
):
    entity = client.get_entity(entity_id=entity_id)

    return entity.dict()
