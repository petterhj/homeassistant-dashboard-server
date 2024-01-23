from asyncio import timeout as async_timeout
from datetime import datetime, timedelta
from json import loads as json_loads
from time import time

from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path as PathParam,
    Query as QueryParam,
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
from ..socket import socket_service_call
from .static import templates


router = APIRouter()


@router.get("")
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
    logger.info(
        "Fetching entity data for {} (history={})".format(
            entity_id,
            history,
        )
    )
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

    logger.debug(f"> Request duration: {round(time() - start_time, 3)} s.")

    if output_format is OutputFormat.html:
        return templates.TemplateResponse(
            "proxy/entity.html",
            {
                "request": request,
                "entity": output,
            },
        )

    return output


@router.get("/service/{domain}/{service}")
async def entity(
    domain: str,
    service: str,
    target: str,
    data: str = None,
    client: HomeAssistantClient = Depends(get_homeassistant_client),
):
    """
    The REST API endpoint for calling services does not currently support
    responses, i.e. for `weather/get_forecast`. Use a websocket connection
    instead.
        https://github.com/home-assistant/core/issues/99820
        https://github.com/home-assistant/core/pull/98610
        https://github.com/zachowj/node-red-contrib-home-assistant-websocket/issues/972
        https://developers.home-assistant.io/docs/api/websocket/#calling-a-service
    """

    try:
        timeout = 2

        async with async_timeout(timeout):
            return await socket_service_call(
                ha_api_url=client.api_url,
                ha_token=client.token,
                domain=domain,
                service=service,
                target={"entity_id": target},
                service_data=json_loads(data) if data else {},
            )
    except TimeoutError as e:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail=f"Home Assistant: Timeout ({timeout} s.)",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Home Assistant: {e}",
        )


@router.get("/calendar")
async def calendar(
    client: HomeAssistantClient = Depends(get_homeassistant_client),
    calendar: list[str] = QueryParam(None),
) -> list[homeassistant.CalendarEvent]:
    now = datetime.now()
    calendar_events = []

    calendars = {
        c["entity_id"]: c["name"]
        for c in _homeassistant_request(client.request, "calendars")
    }

    if calendar and len(calendar) > 0:
        calendars = {
            entity_id: name
            for entity_id, name in calendars.items()
            if entity_id in calendar
        }

    for entity_id, name in calendars.items():
        for event in client.request(
            f"calendars/{entity_id}",
            params={
                "start": now.isoformat(),
                "end": (now + relativedelta(months=3)).isoformat(),
            },
        ):
            event["entity_id"] = entity_id
            event["calendar_name"] = name
            calendar_events.append(event)

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
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not connect to Home Assistant",
        )
