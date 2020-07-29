from abc import abstractmethod
from logging import Logger
from typing import Optional


class OAuthStateStore():
    def __init__(self, logger: Optional[Logger] = None):
        self.logger: Optional[Logger] = logger

    @abstractmethod
    def issue(self) -> str:
        NotImplementedError

    @abstractmethod
    def consume(self, state: str) -> bool:
        NotImplementedError
