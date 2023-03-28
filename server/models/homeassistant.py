from typing import Union
from datetime import datetime

from dateutil import parser
from pydantic import BaseModel, validator


class Config(BaseModel):
    state: str
    version: str
    location_name: str = None
    language: str = None
    country: str = None
    time_zone: str = None
    unit_system: dict = None


class Entity(BaseModel):
    entity_id: str
    state: Union[str, int, float]
    attributes: dict
    last_changed: datetime
    last_updated: datetime
    history: list = None
    history_start: datetime = None
    history_end: datetime = None


class CalendarEvent(BaseModel):
    entity_id: str
    calendar_name: str
    start: datetime
    end: datetime
    summary: str
    description: str = None
    location: str = None

    @validator("start", "end", pre=True)
    def parse_datetime(cls, v):
        return parser.parse(v["dateTime"])
