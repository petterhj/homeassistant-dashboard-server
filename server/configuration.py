from pathlib import Path

from yaml import (
    load as yaml_load,
    SafeLoader,
    ScalarNode,
)
from yamlinclude import YamlIncludeConstructor

from .exceptions import ConfigurationError


def secret_constructor(base_path: Path) -> str:
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
