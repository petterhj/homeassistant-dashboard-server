from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from logging import getLogger
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path as PathParam,
    Request,
    status,
)
from fastapi.templating import Jinja2Templates
from homeassistant_api import Client
from homeassistant_api.errors import (
    EndpointNotFoundError,
    UnauthorizedError,
)
from requests.exceptions import ConnectionError

from .config import get_settings, Settings
from .models import (
    HomeAssistantConfig,
    CalendarEvent,
    OutputFormat,
)

logger = getLogger(__name__)
settings = get_settings()


router = APIRouter(prefix="/ha")
templates = Jinja2Templates(directory="{}/templates".format(
    Path(__file__).parent,
))


async def get_client(
    settings: Settings = Depends(get_settings),
):
    yield Client(
        settings.homeassistant_host,
        settings.homeassistant_token.get_secret_value(),
    )


@router.get("/")
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


@router.get("/config")
async def config(
    client: Client = Depends(get_client),
) -> HomeAssistantConfig:
    try:
        config = client.get_config()
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

    return config


@router.get("/entity/{entity_id}")
async def entity(
    request: Request,
    client: Client = Depends(get_client),
    entity_id: str = PathParam(regex=r"^[0-9A-Za-z\_]+\.[0-9A-Za-z\_]+$"),
    history: bool = False,
    period_start: datetime = None,
    period_end: datetime = None,
    significant_changes_only: bool = False,
    output_format: OutputFormat = OutputFormat.json,
):
    import time
    logger.info("Fetching entity data for {} (history={})".format(
        entity_id,
        history,        
    ))
    start_time = time.time()

    now = datetime.now()
    
    if not period_start:
        period_start = now - timedelta(days=1)
    if not period_end:
        period_end = now

    try:
        entity = client.get_entity(entity_id=entity_id)
        if history:
            history_records = entity.get_history(
                start_timestamp=period_start,
                end_timestamp=period_end,
                significant_changes_only=significant_changes_only,
            )
            history_records = history_records.states if history_records else []
        else:
            history_records = []
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
    
    output = {
        **entity.state.dict(),
        "history": history_records,
        "history_start": period_start.isoformat(timespec="seconds"),
        "history_end": period_end.isoformat(timespec="seconds"),
    }

    logger.info(f"> Request duration: {time.time() - start_time}")
    
    if output_format is OutputFormat.html:
         return templates.TemplateResponse("entity.html", {
            "request": request,
            "entity": output,
        })

    return output


@router.get("/calendar")
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
