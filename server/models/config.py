from enum import Enum
from ipaddress import IPv4Address

from pydantic import (
    BaseModel,
    SecretStr,
    conint,
    confloat,
)

from .server import ServerConfig


class HomeAssistantConfig(BaseModel):
    host: IPv4Address = "127.0.0.1"
    port: int = 8123
    ssl: bool = False
    token: SecretStr = SecretStr("")


class LocaleConfig(BaseModel):
    default: str = None
    fallback: str = None


class DashboardConfig(BaseModel):
    components: list[dict] = [dict(type="sun")]


class CaptureFormat(str, Enum):
    png = "png"
    bmp = "bmp"


class CaptureConfig(BaseModel):
    format: CaptureFormat = CaptureFormat.png
    width: conint(ge=100, le=3000) = None
    height: conint(ge=100, le=3000) = None
    scale: confloat(ge=1.0, le=5.0) = 1.0
    bit_depth: conint(ge=1, le=256) = None
    timeout: conint(ge=1000, le=30000) = 5000
    delay: conint(ge=1, le=30) = None


class Config(BaseModel):
    server: ServerConfig
    homeassistant: HomeAssistantConfig = HomeAssistantConfig()
    timezone: str = None
    locale: LocaleConfig = LocaleConfig()
    dashboard: DashboardConfig = DashboardConfig()
    capture: CaptureConfig = CaptureConfig()
