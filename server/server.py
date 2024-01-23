# https://github.com/samuelcolvin/watchfiles
# https://github.com/encode/uvicorn/blob/master/uvicorn/supervisors/watchfilesreload.py

from pathlib import Path
from socket import socket
from typing import Optional, List, Callable

from fastapi import FastAPI
from uvicorn import Config as UvicornConfig, Server as UvicornServer
from uvicorn.supervisors import Multiprocess
from uvicorn.supervisors.watchfilesreload import (
    FileFilter,
    WatchFilesReload,
)
from watchfiles import watch

from .models.server import ServerConfig


class Reloader(WatchFilesReload):
    def __init__(
        self,
        config: UvicornConfig,
        target: Callable[[Optional[List[socket]]], None],
        sockets: List[socket],
    ) -> None:
        super().__init__(config, target, sockets)

        if config.reload_dirs:
            self.reload_dirs = config.reload_dirs
        else:
            self.reload_dirs.append(Path.cwd())

        self.watch_filter = FileFilter(config)
        self.watcher = watch(
            *self.reload_dirs,
            watch_filter=None,
            stop_event=self.should_exit,
            # using yield_on_timeout here mostly to make sure tests don't
            # hang forever, won't affect the class's behavior
            yield_on_timeout=True,
        )

    def should_restart(self) -> Optional[List[Path]]:
        changes = next(self.watcher)
        if changes:
            unique_paths = {Path(c[1]) for c in changes}
            return [p for p in unique_paths if self.watch_filter(p)]
        return None


class Server:
    def __init__(self, app: FastAPI, server_config: ServerConfig):
        reload_config = {
            "reload": True,
            "reload_includes": ["*.yml", "*.yaml"],
            "reload_dirs": [server_config.data_path.resolve()],
        }
        if server_config.debug:
            reload_config["reload_includes"].extend(["*.py", "*.html"])
            reload_config["reload_dirs"].append("./server/")

        self.config = UvicornConfig(
            "server.app:app",
            host=str(server_config.host),
            port=server_config.port,
            log_level="debug" if server_config.debug else "info",
            **reload_config,
        )

        self.server = UvicornServer(config=self.config)
        self.server.force_exit = False
        self.supervisor_type = None

        if self.config.should_reload:
            self.supervisor_type = Reloader
        if self.config.workers > 1:
            self.supervisor_type = Multiprocess

    def run(self):
        if self.supervisor_type:
            sock = self.config.bind_socket()
            supervisor = self.supervisor_type(
                self.config,
                target=self.server.run,
                sockets=[sock],
            )
            supervisor.run()
        else:
            self.server.run()
