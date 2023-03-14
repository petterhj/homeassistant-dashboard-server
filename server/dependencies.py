import json
from functools import lru_cache
from pathlib import Path

from fastapi import Depends, HTTPException, status
from homeassistant_api import Client as HomeAssistantClient
from loguru import logger
from pydantic import ValidationError
from yaml import (
    SafeLoader,
    load as yaml_load,
    ScalarNode,
)
from yamlinclude import YamlIncludeConstructor

from .exceptions import ConfigurationError
from .models.config import Config
from .models.server import ServerConfig


def secret_constructor(base_path) -> str:
    """Read secret from secrets file."""
    def _get_secret(loader: SafeLoader, node: ScalarNode) -> str:
        secrets_file_path = base_path / 'secrets.yaml'
        
        if not secrets_file_path.exists():
            raise ConfigurationError(
                f"Could not locate {secrets_file_path.resolve()}",
            )

        with open(secrets_file_path, "r") as secrets_file:
            secrets = yaml_load(secrets_file, Loader=SafeLoader)

            if not secrets.get(node.value):
                raise ConfigurationError(
                    f"Secret `{node.value}` not found in `secrets.yaml`"
                )

            return secrets.get(node.value)

    return _get_secret


def yaml_loader(base_path: Path):
    """Add constructors to the PyYAML loader."""
    loader = SafeLoader
    YamlIncludeConstructor.add_to_loader_class(
        loader_class=loader,
        base_dir=base_path,
    )
    loader.add_constructor(u"!secret", secret_constructor(base_path))
    return loader


@lru_cache()
def get_config() -> Config:
    def _raise_error(detail):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

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

    except ValidationError as e:
        _raise_error(json.loads(e.json()))
    except FileNotFoundError:
        return Config(server=server_config)
    except ConfigurationError as e:
        _raise_error(str(e))


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
