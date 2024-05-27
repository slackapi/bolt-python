from http import HTTPStatus
from typing import Dict, Iterable, List, Sequence, Tuple

from .internals import ENCODING


class WsgiHttpResponse:
    """This Class uses the PEP 3333 standard to adapt bolt response information
    for the WSGI web server running the application

    PEP 3333: https://peps.python.org/pep-3333/
    """

    __slots__ = ("status", "_headers", "_body")

    def __init__(self, status: int, headers: Dict[str, Sequence[str]] = {}, body: str = ""):
        _status = HTTPStatus(status)
        self.status = f"{_status.value} {_status.phrase}"
        self._headers = headers
        self._body = bytes(body, ENCODING)

    def get_headers(self) -> List[Tuple[str, str]]:
        headers: List[Tuple[str, str]] = []
        for key, value in self._headers.items():
            if key.lower() == "content-length":
                continue
            headers.append((key, value[0]))

        headers.append(("content-length", str(len(self._body))))
        return headers

    def get_body(self) -> Iterable[bytes]:
        return [self._body]
