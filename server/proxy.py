from datetime import datetime
from dateutil.relativedelta import relativedelta

from fastapi import APIRouter, Depends, HTTPException, Path, status
from homeassistant_api import Client
from homeassistant_api.errors import EndpointNotFoundError, UnauthorizedError
from requests.exceptions import ConnectionError

from .config import get_settings, Settings
from .models import CalendarEvent


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
    entity_id: str = Path(regex=r"^[0-9A-Za-z\_]+\.[0-9A-Za-z\_]+$"),
    history: bool = False,
):
    try:
        entity = client.get_entity(entity_id=entity_id)
        history = entity.get_history().states if history else []
    except EndpointNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity `{entity_id}` not found",
        )
    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not connect to Home Assistant",
        )

    return {
        **entity.state.dict(),
        "history": history,
    }


@router.get("/ha/calendar")
async def calendar(
    client: Client = Depends(get_client),
):
    now = datetime.now()
    calendar_events = []

    try:
        for calendar in client.request("calendars"):
            entity_id = calendar['entity_id']
            for event in client.request(f"calendars/{entity_id}", params={
                "start": now.isoformat(),
                "end": (now + relativedelta(months=3)).isoformat(),
            }):
                event["entity_id"] = entity_id
                event["calendar_name"] = calendar["name"]
                calendar_events.append(
                    CalendarEvent.parse_obj(event)
                )
    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not connect to Home Assistant",
        )

    calendar_events.sort(key=lambda event: event.start)

    return [event.dict() for event in calendar_events]
