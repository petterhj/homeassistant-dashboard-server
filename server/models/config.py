from ipaddress import IPv4Address

from pydantic import BaseModel, SecretStr

from .server import ServerConfig


class HomeAssistantConfig(BaseModel):
    host: IPv4Address
    port: int = 8123
    ssl: bool = False
    token: SecretStr


class LocaleConfig(BaseModel):
    default: str = None
    fallback: str = None


class DashboardConfig(BaseModel):
    components: list[dict] = None


class Config(BaseModel):
    server: ServerConfig
    homeassistant: HomeAssistantConfig
    timezone: str = None
    locale: LocaleConfig
    dashboard: DashboardConfig
