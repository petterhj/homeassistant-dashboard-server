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
    capture_interval: conint(ge=60) = 60 * 3
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
