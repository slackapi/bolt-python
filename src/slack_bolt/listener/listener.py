from abc import abstractmethod, ABCMeta
from typing import List

from slack_bolt.listener_matcher import ListenerMatcher
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class Listener(metaclass=ABCMeta):
    matchers: List[ListenerMatcher] = []

    def matches(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse) -> bool:
        is_matched: bool = False
        for matcher in self.matchers:
            is_matched = matcher.matches(req, resp)
            if not is_matched:
                return is_matched
        return is_matched

    @abstractmethod
    def __call__(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse) -> BoltResponse:
        raise NotImplementedError
