from abc import abstractmethod, ABCMeta
from typing import List

from slack_bolt.listener_matcher.async_listener_matcher import AsyncListenerMatcher
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


class AsyncListener(metaclass=ABCMeta):
    matchers: List[AsyncListenerMatcher]
    middleware: List[AsyncMiddleware]
    auto_acknowledgement: bool

    async def async_matches(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
    ) -> bool:
        is_matched: bool = False
        for matcher in self.matchers:
            is_matched = await matcher.async_matches(req, resp)
            if not is_matched:
                return is_matched
        return is_matched

    async def run_async_middleware(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
    ) -> (BoltResponse, bool):
        """

        :param req: the incoming request
        :param resp: the current response
        :return: a tuple of the processed response and a flag indicating termination
        """
        for m in self.middleware:
            middleware_state = {"next_called": False}

            async def _next():
                middleware_state["next_called"] = True

            resp = await m.async_process(req=req, resp=resp, next=_next)
            if not middleware_state["next_called"]:
                # next() was not called in this middleware
                return (resp, True)
        return (resp, False)

    @abstractmethod
    async def __call__(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse) -> BoltResponse:
        """Runs all the registered middleware and then run the listener function.

        :param req: the incoming request
        :param resp: the current response
        :return: the processed response
        """
        raise NotImplementedError()
