import json
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from homeassistant_api import Client as HomeAssistantClient
from loguru import logger
from yaml import load as yaml_load

from .configuration import yaml_loader
from .exceptions import ConfigurationError
from .models.config import Config
from .models.server import ServerConfig


@lru_cache()
def get_config() -> Config:
    try:
        server_config = ServerConfig()

        logger.info(f"Reading config from `{server_config.config_file}`")

        with open(server_config.config_file, "r") as config_file:
            yaml_config = yaml_load(config_file, Loader=yaml_loader(
                base_path=server_config.config_file.parent
            ))

            if "server" in yaml_config:
                logger.warning("The `server` key cannot be configured using YAML")
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
    yield HomeAssistantClient(
        "{}://{}:{}/api".format(
            'https' if config.homeassistant.ssl else 'http',
            config.homeassistant.host,
            config.homeassistant.port,
        ),
        config.homeassistant.token.get_secret_value(),
    )