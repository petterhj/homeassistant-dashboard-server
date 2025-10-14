from functools import lru_cache

from fastapi import Depends, HTTPException, status
from homeassistant_api import Client as HomeAssistantClient
from loguru import logger
from yaml import load as yaml_load, scanner

from .configuration import yaml_loader
from .exceptions import ConfigurationError
from .models.capture import Capture
from .models.config import Config, CaptureFormat
from .models.server import ServerConfig
from .models.view import View


@lru_cache()
def get_config() -> Config:
    try:
        server_config = ServerConfig()

        logger.info(f"Reading config from `{server_config.config_file}`")

        with open(server_config.config_file, "r") as config_file:
            try:
                yaml_config = yaml_load(
                    config_file,
                    Loader=yaml_loader(base_path=server_config.config_file.parent),
                )
            except scanner.ScannerError as e:
                raise ConfigurationError(f"Invalid configuration: {e}")

            if not yaml_config:
                logger.warning("Configuration file empty, using defaults")
                return Config(server=server_config)

            if "server" in yaml_config:
                logger.warning(
                    "The `server` key cannot be configured using YAML"
                )
                del yaml_config["server"]

            return Config(server=server_config, **yaml_config)

    except FileNotFoundError:
        logger.warning("Configuration file not found, using defaults")
        return Config(server=server_config)


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


def get_view(
    view_name: str,
    config: Config = Depends(get_config),
) -> View:
    views = {v.name: v for v in config.views}

    if view_config := views.get(view_name):
        captures = []
        capture_path = config.server.capture_path

        for fmt in CaptureFormat:
            captures.extend(
                Capture(
                    timestamp=int(capture_file.name.split("_")[0]),
                    filename=capture_file.name,
                    format=fmt
                )
                for capture_file in capture_path.glob(
                    f"*_{view_name}.{fmt.value}"
                )
                if "_tmp" not in capture_file.name
            )

        return View(
            name=view_config.name,
            captures=sorted(captures, key=lambda c: c.timestamp, reverse=True),
            config=view_config,
        )

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"View '{view_name}' not found",
        )


def get_views(
    config: Config = Depends(get_config),
):
    return [get_view(view_config.name, config) for view_config in config.views]
