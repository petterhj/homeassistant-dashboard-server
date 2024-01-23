import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from loguru import logger
from pydantic import ValidationError

from .logger import configure_logger
from .models.server import ServerConfig
from .server import Server


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--data-path", type=Path, required=False)
    args = parser.parse_args()

    if args.data_path:
        os.environ["DATA_PATH"] = str(args.data_path)

    try:
        config = ServerConfig()
    except ValidationError as e:
        print("Configuration error:")
        print(str(e))
        sys.exit(1)

    configure_logger(config)

    logger.info("Starting server...")
    for name, value in config.dict().items():
        logger.info(f"> {name}: {value}")

    Server("app", config).run()
