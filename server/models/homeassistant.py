from typing import Union, Optional
from datetime import datetime

from dateutil import parser
from pydantic import BaseModel, validator


class Config(BaseModel):
    state: str
    version: str
    location_name: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None
    time_zone: Optional[str] = None
    unit_system: Optional[dict] = None


class Entity(BaseModel):
    entity_id: str
    state: Union[str, int, float]
    attributes: dict
    last_changed: datetime
    last_updated: datetime
    history: Optional[list] = None
    history_start: Optional[datetime] = None
    history_end: Optional[datetime] = None


class CalendarEvent(BaseModel):
    entity_id: str
    calendar_name: str
    start: datetime
    end: datetime
    summary: str
    description: Optional[str] = None
    location: Optional[str] = None

    @validator("start", "end", pre=True)
    def parse_datetime(cls, v):
        if v.get("dateTime"):
            return parser.parse(v["dateTime"])
        if v.get("date"):
            return parser.parse(v["date"])
