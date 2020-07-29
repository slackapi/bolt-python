from abc import abstractmethod, ABCMeta
from typing import List

from slack_bolt.listener_matcher import ListenerMatcher
from slack_bolt.middleware import Middleware
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class Listener(metaclass=ABCMeta):
    matchers: List[ListenerMatcher] = []
    middleware: List[Middleware] = []
    auto_acknowledgement: bool = False

    def matches(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
    ) -> bool:
        is_matched: bool = False
        for matcher in self.matchers:
            is_matched = matcher.matches(req, resp)
            if not is_matched:
                return is_matched
        return is_matched

    def run_middleware(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
    ) -> (BoltResponse, bool):
        """

        :param req: the incoming request
        :param resp: the current response
        :return: a tuple of the processed response and a flag indicating termination
        """
        for m in self.middleware:
            middleware_state = {"next_called": False}

            def next():
                middleware_state["next_called"] = True

            resp = m.process(req=req, resp=resp, next=next)
            if not middleware_state["next_called"]:
                # next() was not called in this middleware
                return (resp, True)
        return (resp, False)

    @abstractmethod
    def __call__(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse) -> BoltResponse:
        """Runs all the registered middleware and then run the listener function.

        :param req: the incoming request
        :param resp: the current response
        :return: the processed response
        """
        raise NotImplementedError()
