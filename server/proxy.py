from fastapi import APIRouter, Depends, HTTPException, Path, status
from homeassistant_api import Client
from homeassistant_api.errors import UnauthorizedError
from requests.exceptions import ConnectionError

from .config import get_settings, Settings


router = APIRouter()

async def get_client(
    settings: Settings = Depends(get_settings),
):
    yield Client(
        settings.homeassistant_host,
        settings.homeassistant_token.get_secret_value(),
    )

@router.get("/ha")
async def check_ha_api(
    client: Client = Depends(get_client),
):
    try:
        api_running = client.check_api_running()
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not connect to Home Assistant",
        )

    return {"running": api_running}


@router.get("/ha/entity/{entity_id}")
async def entity(
    client: Client = Depends(get_client),
    entity_id: str = Path(regex=r"^[0-9A-Za-z\_]+\.[0-9A-Za-z\_]+$")
):
    try:
        entity = client.get_entity(entity_id=entity_id)
    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not connect to Home Assistant",
        )

    return entity.dict()
