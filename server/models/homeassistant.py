from datetime import datetime

from dateutil import parser
from pydantic import BaseModel, field_validator


class Config(BaseModel):
    state: str
    version: str
    location_name: str | None = None
    language: str | None = None
    country: str | None = None
    time_zone: str | None = None
    unit_system: dict | None = None


class Entity(BaseModel):
    entity_id: str
    state: str | int | float
    attributes: dict
    last_changed: datetime
    last_updated: datetime
    history: list | None = None
    history_start: datetime | None = None
    history_end: datetime | None = None


class CalendarEvent(BaseModel):
    entity_id: str
    calendar_name: str
    start: datetime
    end: datetime
    summary: str
    description: str | None = None
    location: str | None = None

    @field_validator("start", "end", mode="before")
    @classmethod
    def parse_datetime(cls, v):
        if isinstance(v, dict):
            if v.get("dateTime"):
                return parser.parse(v["dateTime"])
            if v.get("date"):
                return parser.parse(v["date"])
        return v
