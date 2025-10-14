from datetime import datetime
from enum import Enum

from pydantic import BaseModel, computed_field


class CaptureFormat(str, Enum):
    png = "png"
    bmp = "bmp"


class Capture(BaseModel):
    timestamp: int
    filename: str
    format: CaptureFormat

    @computed_field
    @property
    def datetime(self) -> str:
        return datetime.fromtimestamp(self.timestamp).isoformat()


class CaptureDetails(Capture):
    file_size: int = None
    mime_type: str = None
    resolution: tuple[int, int] = None
    mode: str = None
    bit_depth: int = None
    has_transparency: bool | None = None
    palette_size: int | None = None
    compression: int | None = None
