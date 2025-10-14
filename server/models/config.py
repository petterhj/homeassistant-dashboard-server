from enum import Enum
from os import environ
from typing import Annotated

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    SecretStr,
    Field,
)

from .server import ServerConfig
from .capture import CaptureFormat


class HomeAssistantConfig(BaseModel):
    url: AnyHttpUrl = "http://127.0.0.1:8123"
    token: SecretStr = SecretStr("")


class LocaleConfig(BaseModel):
    default: str = None
    fallback: str = None


class ContainerConfig(BaseModel):
    style: str | None = None
    show_footer: bool = True


class ViewConfig(BaseModel):
    name: str = "dashboard"
    style: str | None = None
    components: list[dict] = [dict(type="sun")]


class CaptureWaitUntil(str, Enum):
    load = "load"
    domcontentloaded = "domcontentloaded"
    networkidle = "networkidle"
    commit = "commit"


class CaptureConfig(BaseModel):
    format: CaptureFormat = CaptureFormat.png
    width: Annotated[int, Field(ge=100, le=3000)] = 1200  # Inkplate 10
    height: Annotated[int, Field(ge=100, le=3000)] = 825
    scale: Annotated[float, Field(ge=1.0, le=5.0)] = 1

    invert: bool = False
    grayscale: bool = True

    delay: Annotated[int, Field(ge=1000, le=30000)] | None = None
    timeout: Annotated[int, Field(ge=1000, le=30000)] = 5000
    wait_until: CaptureWaitUntil = CaptureWaitUntil.networkidle


class Config(BaseModel):
    server: ServerConfig
    homeassistant: HomeAssistantConfig = HomeAssistantConfig()
    timezone: str = None
    locale: LocaleConfig = LocaleConfig()
    container: ContainerConfig = ContainerConfig()
    views: list[ViewConfig] = [ViewConfig()]
    capture: CaptureConfig = CaptureConfig()
    version: str = environ.get("APP_VERSION")
