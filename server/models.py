from datetime import datetime

from dateutil import parser
from pydantic import BaseModel, validator


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
