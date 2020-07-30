from abc import ABCMeta, abstractmethod
from typing import Callable, Awaitable

from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class AsyncMiddleware(metaclass=ABCMeta):

    @abstractmethod
    async def async_process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        raise NotImplementedError()

    @property
    def name(self) -> str:
        return f"{self.__module__}.{self.__class__.__name__}"
