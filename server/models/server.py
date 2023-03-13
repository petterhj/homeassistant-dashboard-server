from enum import Enum
from ipaddress import IPv4Address
from pathlib import Path

from pydantic import (
    BaseModel,
    BaseSettings,
    DirectoryPath,
    root_validator,
)


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
    host: IPv4Address= '127.0.0.1'
    port: int = 8089
    log_level: ServerLogLevel = ServerLogLevel.info
    log_filename: Path = "dashboard.log"
    log_json: bool = False
    static_path: Path = "dist"

    class Config:
        env_file = ".env"

    @root_validator
    def check_paths(cls, values):
        if "data_path" in values:
            filename = Path(values["config_filename"]).name
            filepath = Path(values["data_path"] / filename).resolve()
            if filepath.exists():
                values["config_filename"] = str(filename)
            else:
                raise ValueError(f"File `{filepath}` does not exist")
        return values
    
    @property
    def config_file(self) -> Path:
        return self.data_path.resolve() / self.config_filename


class ScreenshotConfig(BaseModel):
    width: int = None
    height: int = None
    scale: int = 1
    timeout: int = 5000
    delay: int = 0


class OutputFormat(str, Enum):
    json = "json"
    html = "html"
    png = "png"
