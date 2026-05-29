from typing import Iterable, Sequence, Tuple, Dict, Union, List

from .utils import ENCODING


class AsgiHttpResponse:
    __slots__ = ("status", "raw_headers", "body")

    def __init__(self, status: int, headers: Dict[str, Sequence[str]] = {}, body: str = ""):
        self.status: int = status
        self.body: bytes = bytes(body, ENCODING)
        self.raw_headers: List[Tuple[bytes, bytes]] = [
            (bytes(key, ENCODING), bytes(v, ENCODING))
            for key, values in headers.items()
            if key.lower() != "content-length"
            for v in values
        ]
        self.raw_headers.append((b"content-length", bytes(str(len(self.body)), ENCODING)))

    def get_response_start(self) -> Dict[str, Union[str, int, Iterable[Tuple[bytes, bytes]]]]:
        return {
            "type": "http.response.start",
            "status": self.status,
            "headers": self.raw_headers,
        }

    def get_response_body(self) -> Dict[str, Union[str, bytes, bool]]:
        return {
            "type": "http.response.body",
            "body": self.body,
            "more_body": False,
        }
