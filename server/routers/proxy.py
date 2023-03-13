from time import time
from datetime import datetime, timedelta

from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path as PathParam,
    Request,
    status,
)
from homeassistant_api import Client as HomeAssistantClient
from homeassistant_api.errors import (
    EndpointNotFoundError,
    UnauthorizedError,
)
from loguru import logger
from requests.exceptions import ConnectionError

from ..models import homeassistant
from ..models.server import OutputFormat
from ..dependencies import get_homeassistant_client
from .static import templates


router = APIRouter()


@router.get("/")
async def config(
    client: HomeAssistantClient = Depends(get_homeassistant_client),
) -> homeassistant.Config:
    return _homeassistant_request(client.get_config)


@router.get("/entity/{entity_id}")
async def entity(
    request: Request,
    client: HomeAssistantClient = Depends(get_homeassistant_client),
    entity_id: str = PathParam(regex=r"^[0-9A-Za-z\_]+\.[0-9A-Za-z\_]+$"),
    history: bool = False,
    period_start: datetime = None,
    period_end: datetime = None,
    significant_changes_only: bool = False,
    output_format: OutputFormat = OutputFormat.json,
) -> homeassistant.Entity:
    logger.info("Fetching entity data for {} (history={})".format(
        entity_id,
        history,        
    ))
    start_time = time()

    entity = _homeassistant_request(client.get_entity, entity_id=entity_id)

    output = {
        **entity.state.dict(),
    }

    if history:
        now = datetime.now()
            
        if not period_start:
            period_start = now - timedelta(days=1)
        if not period_end:
            period_end = now

        history_records = entity.get_history(
            start_timestamp=period_start,
            end_timestamp=period_end,
            significant_changes_only=significant_changes_only,
        )

        output = {
            **output,
            "history": history_records.states if history_records else [],
            "history_start": period_start.isoformat(timespec="seconds"),
            "history_end": period_end.isoformat(timespec="seconds"),
        }

    logger.debug(f"> Request duration: {time() - start_time}")
    
    if output_format is OutputFormat.html:
         return templates.TemplateResponse("proxy/entity.html", {
            "request": request,
            "entity": output,
        })

    return output



@router.get("/calendar")
async def calendar(
    client: HomeAssistantClient = Depends(get_homeassistant_client),
) -> list[homeassistant.CalendarEvent]:
    now = datetime.now()
    calendar_events = []

    calendars = _homeassistant_request(client.request, "calendars")

    for calendar in calendars:
        entity_id = calendar['entity_id']
        for event in client.request(f"calendars/{entity_id}", params={
            "start": now.isoformat(),
            "end": (now + relativedelta(months=3)).isoformat(),
        }):
            event["entity_id"] = entity_id
            event["calendar_name"] = calendar["name"]
            calendar_events.append(event)
    
    calendar_events.sort(key=lambda event: date_parser.parse(event["start"]["dateTime"]))

    return calendar_events


def _homeassistant_request(method, *args, **kwargs):
    try:
        return method(*args, **kwargs)
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Home Assistant: {e}",
        )
    except EndpointNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Home Assistant: {e} (endpoint not found)",
        )
    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not connect to Home Assistant",
        )
