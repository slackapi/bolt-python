from abc import abstractmethod, ABCMeta

from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


class AsyncListenerMatcher(metaclass=ABCMeta):

    @abstractmethod
    async def async_matches(self, req: AsyncBoltRequest, resp: BoltResponse) -> bool:
        raise NotImplementedError()
