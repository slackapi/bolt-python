from abc import ABCMeta, abstractmethod
from typing import Callable

from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class Middleware(metaclass=ABCMeta):
    @abstractmethod
    def process(
        self, *, req: BoltRequest, resp: BoltResponse, next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        raise NotImplementedError()

    @property
    def name(self) -> str:
        return f"{self.__module__}.{self.__class__.__name__}"
