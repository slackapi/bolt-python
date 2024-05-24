from typing import Sequence, Tuple, Dict, List
from http import HTTPStatus

from .utils import ENCODING


class WsgiHttpResponse:
    __slots__ = ("status", "headers", "body")

    def __init__(self, status: int, headers: Dict[str, Sequence[str]] = {}, body: str = ""):
        _status = HTTPStatus(status)
        self.status = f"{_status.value} {_status.phrase}"

        self.headers: List[Tuple[str, str]] = []
        for key, value in headers.items():
            if key.lower() == "content-length":
                continue
            self.headers.append((key, value[0]))

        _body = bytes(body, ENCODING)
        self.headers.append(("content-length", str(len(_body))))
        self.body = [_body]
