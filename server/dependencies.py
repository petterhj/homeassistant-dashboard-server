from pathlib import Path
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from homeassistant_api import Client as HomeAssistantClient
from loguru import logger
from yaml import load as yaml_load

from .configuration import yaml_loader
from .exceptions import ConfigurationError
from .models.config import Config, CaptureFormat
from .models.server import ServerConfig


@lru_cache()
def get_config() -> Config:
    try:
        server_config = ServerConfig()

        logger.info(f"Reading config from `{server_config.config_file}`")

        with open(server_config.config_file, "r") as config_file:
            yaml_config = yaml_load(
                config_file,
                Loader=yaml_loader(base_path=server_config.config_file.parent),
            )

            if "server" in yaml_config:
                logger.warning(
                    "The `server` key cannot be configured using YAML"
                )
                del yaml_config["server"]

            return Config(server=server_config, **yaml_config)

    except FileNotFoundError:
        logger.warning("Configuration file not found, using defaults")
        return Config(server=server_config)
    except ConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def get_homeassistant_client(
    config: Config = Depends(get_config),
) -> HomeAssistantClient:
    ha_url = str(config.homeassistant.url)
    if ha_url.endswith("/"):
        ha_url = ha_url[:-1]
    yield HomeAssistantClient(
        f"{ha_url}/api",
        config.homeassistant.token.get_secret_value(),
    )


def get_captures(
    capture_format: CaptureFormat,
    capture_name: str = "dashboard",
    config: dict = Depends(get_config),
) -> list[Path]:
    capture_path = config.server.capture_path
    capture_files = sorted(
        [
            capture_file
            for capture_file in capture_path.glob(
                f"*_{capture_name}.{capture_format.value}"
            )
            if "_tmp" not in capture_file.name
        ],
        reverse=True,
    )
    return capture_files
