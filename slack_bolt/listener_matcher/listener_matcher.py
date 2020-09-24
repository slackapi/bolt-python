from abc import abstractmethod, ABCMeta

from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class ListenerMatcher(metaclass=ABCMeta):
    @abstractmethod
    def matches(self, req: BoltRequest, resp: BoltResponse) -> bool:
        """Matches against the request and returns True if matched.

        :param req: The request
        :param resp: The response
        :return: True if matched.
        """
        raise NotImplementedError()
