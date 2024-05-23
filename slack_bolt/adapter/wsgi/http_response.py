from typing import Iterable, Sequence, Tuple, Dict, List

from .utils import ENCODING
from http import HTTPStatus

class WsgiHttpResponse:
    __slots__ = ("status", "raw_headers", "body")

    def __init__(self, status: int, headers: Dict[str, Sequence[str]] = {}, body: str = ""):
        _status = HTTPStatus(status)
        self.status = f"{_status.value} {_status.phrase.upper()}"
        self.raw_headers: List[Tuple[str, str]] = [
            (key, value[0]) for key, value in headers.items()
        ]
        self.raw_headers.append(("content-length", str(len(body))))
        self.body = [bytes(body, ENCODING)]
