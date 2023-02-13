from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8089
    screenshot_path: Path = "data/temp.png"
    screenshot_fallback_path: Path = "data/fallback.jpg"
    screenshot_timeout: int = 1000
    screenshot_width: int = 1200
    screenshot_height: int = 825
    tz: str = "Europe/Oslo"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
