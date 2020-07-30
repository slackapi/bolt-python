from logging import Logger
from pathlib import Path

from .oauth_state_store import OAuthStateStore


class FileOAuthStateStore(OAuthStateStore):

    def __init__(
        self,
        *,
        logger: Logger,
        base_dir: str = str(Path.home()) + "/.bolt-app-oauth-state",
    ):
        self.logger = logger
        self.base_dir = base_dir

    def issue(self) -> str:
        # TODO: implement this
        return "dummy"

    def consume(self, state: str) -> bool:
        # TODO: implement this
        return True
