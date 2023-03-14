from ipaddress import IPv4Address

from pydantic import BaseModel, SecretStr

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


class Config(BaseModel):
    server: ServerConfig
    homeassistant: HomeAssistantConfig = HomeAssistantConfig()
    timezone: str = None
    locale: LocaleConfig = LocaleConfig()
    dashboard: DashboardConfig = DashboardConfig()
