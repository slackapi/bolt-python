from typing import Callable, Iterable, Tuple, Dict, Union

ENCODING = "latin-1"  # should always be encoded in ISO-8859-1


class AsgiHttpRequest:
    def __init__(self, scope: Dict[str, Union[str, bytes, Iterable[Tuple[bytes, bytes]]]], receive: Callable):
        self.receive = receive
        self.scope = scope

    @property
    def method(self) -> str:
        return self.scope["method"]

    @property
    def path(self) -> str:
        return self.scope["path"]

    @property
    def query_string(self) -> str:
        raw_query_string: bytes = self.scope["query_string"]
        return raw_query_string.decode(ENCODING)

    @property
    def headers(self) -> Dict[str, str]:
        raw_headers: Iterable[Tuple[bytes, bytes]] = self.scope.get("headers", [])
        return {header[0].decode(ENCODING): header[1].decode(ENCODING) for header in raw_headers}

    async def get_raw_body(self) -> str:
        chunks = bytearray()
        while True:
            chunk: Dict[str, Union[str, bytes]] = await self.receive()

            if chunk.get("type") != "http.request":
                raise Exception("Body chunks could not be received from asgi server")

            chunks.extend(chunk.get("body", b""))
            if not chunk.get("more_body", False):
                break
        return bytes(chunks).decode(ENCODING)
