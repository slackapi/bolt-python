from abc import ABCMeta, abstractmethod
from typing import Callable, Awaitable, Optional

from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


class AsyncMiddleware(metaclass=ABCMeta):
    @abstractmethod
    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> Optional[BoltResponse]:
        raise NotImplementedError()

    @property
    def name(self) -> str:
        return f"{self.__module__}.{self.__class__.__name__}"
