from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, HttpUrl, SecretStr


class Settings(BaseSettings):
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8089
    static_path: Path = "frontend/dist"
    static_fallback_path: Path = "data/fallback"
    homeassistant_host: HttpUrl
    homeassistant_token: SecretStr
    dashboard_config: Path = "config.yml"
    screenshot_path: Path = "data/temp.png"
    screenshot_timeout: int = 3000
    screenshot_delay: int = 500
    screenshot_width: int = 1200
    screenshot_height: int = 825
    screenshot_scaling: int = 1
    tz: str = "Europe/Oslo"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
