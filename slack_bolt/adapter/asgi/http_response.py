from typing import Iterable, Sequence, Tuple, Dict, Union

ENCODING = "utf-8"  # should always be utf-8


class AsgiHttpResponse:
    def __init__(self, status: int, headers: Dict[str, Sequence[str]] = {}, body: str = ""):
        self.status = status
        self.headers = headers
        self.body = body

    @ property
    def raw_headers(self) -> Iterable[Tuple[bytes, bytes]]:
        headers = [(bytes(key, ENCODING), bytes(value[0], ENCODING)) for key, value in self.headers.items()]
        headers.append((b"content-length", bytes(str(len(self.body)), ENCODING)))
        return headers

    def get_response_start(self) -> Dict[str, Union[str, int, Iterable[Tuple[bytes, bytes]]]]:
        return {
            "type": "http.response.start",
            "status": self.status,
            "headers": self.raw_headers,
        }

    def get_response_body(self) -> Dict[str, Union[str, bytes, bool]]:
        return {
            "type": "http.response.body",
            "body": bytes(self.body, ENCODING),
            "more_body": False,
        }
