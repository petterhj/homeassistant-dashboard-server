from pydantic import BaseModel, Field, computed_field


from .capture import Capture
from .config import ViewConfig


class View(BaseModel):
    name: str
    captures: list[Capture] = Field(default_factory=list)
    config: ViewConfig

    @computed_field
    @property
    def last_capture(self) -> Capture | None:
        return max(self.captures, key=lambda c: c.timestamp)
