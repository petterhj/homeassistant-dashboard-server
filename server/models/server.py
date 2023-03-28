from enum import Enum
from ipaddress import IPv4Address
from pathlib import Path

from pydantic import (
    BaseModel,
    BaseSettings,
    confloat,
    conint,
    DirectoryPath,
    root_validator,
)


class OutputFormat(str, Enum):
    json = "json"
    html = "html"


class ServerLogLevel(str, Enum):
    critical = "critical"
    error = "error"
    warning = "warning"
    info = "info"
    debug = "debug"


class ServerConfig(BaseSettings):
    data_path: DirectoryPath = "data"
    config_filename: str = "configuration.yaml"
    debug: bool = False
    host: IPv4Address= "127.0.0.1"
    port: int = 8089
    capture_interval: conint(ge=60) = 60#5 * 60
    capture_keep_count: conint(ge=1) = 15
    log_level: ServerLogLevel = ServerLogLevel.info
    log_filename: Path = "dashboard.log"
    log_json: bool = False
    static_path: Path = "dist"

    class Config:
        env_file = ".env"
    
    @property
    def config_file(self) -> Path:
        return self.data_path.resolve() / self.config_filename

    @property
    def capture_path(self) -> DirectoryPath:
        return self.data_path.resolve() / "captures"


class ScreenshotConfig(BaseModel): # TODO: Remove
    width: conint(ge=100, le=3000) = None
    height: conint(ge=100, le=3000) = None
    scale: confloat(ge=1.0, le=5.0) = 1.0
    timeout: conint(ge=1000, le=30000) = 5000
    delay: conint(ge=1, le=30) = None

    @root_validator(skip_on_failure=True)
    def check_values(cls, values):
        if values["width"] or values["height"]:
            if not values["width"] or not values["height"]:
                raise ValueError(
                    "Both `width` and `height` must be specified when scaling",
                )
        return values
