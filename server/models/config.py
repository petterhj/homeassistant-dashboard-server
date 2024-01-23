from enum import Enum
from ipaddress import IPv4Address
from os import environ

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    SecretStr,
    conint,
    confloat,
)

from .server import ServerConfig


class HomeAssistantConfig(BaseModel):
    url: AnyHttpUrl = "http://127.0.0.1:8123"
    token: SecretStr = SecretStr("")


class LocaleConfig(BaseModel):
    default: str = None
    fallback: str = None


class DashboardConfig(BaseModel):
    components: list[dict] = [dict(type="sun")]


class CaptureFormat(str, Enum):
    png = "png"
    bmp = "bmp"


class CaptureWaitUntil(str, Enum):
    load = "load"
    domcontentloaded = "domcontentloaded"
    networkidle = "networkidle"
    commit = "commit"


class CaptureConfig(BaseModel):
    format: CaptureFormat = CaptureFormat.png
    width: conint(ge=100, le=3000) = None
    height: conint(ge=100, le=3000) = None
    scale: confloat(ge=1.0, le=5.0) = 1.0
    invert: bool = False
    grayscale: bool = False
    bit_depth: conint(ge=1, le=256) = None
    delay: conint(ge=1000, le=30000) = None
    timeout: conint(ge=1000, le=30000) = 5000
    wait_until: CaptureWaitUntil = CaptureWaitUntil.networkidle


class RemoteConfig(BaseModel):
    url: AnyHttpUrl
    capture: CaptureConfig = None


class Config(BaseModel):
    server: ServerConfig
    homeassistant: HomeAssistantConfig = HomeAssistantConfig()
    timezone: str = None
    locale: LocaleConfig = LocaleConfig()
    dashboard: DashboardConfig = DashboardConfig()
    remote: dict[str, RemoteConfig] = None
    capture: CaptureConfig = CaptureConfig()
    version: str = environ.get("APP_VERSION")
