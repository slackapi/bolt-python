from typing import Callable, Iterable, Tuple, Dict, Union

ENCODING = "latin-1"  # should always be encoded in ISO-8859-1


class AsgiHttpRequest:
    __slots__ = ("receive", "query_string", "raw_headers")

    def __init__(self, scope: Dict[str, Union[str, bytes, Iterable[Tuple[bytes, bytes]]]], receive: Callable):
        self.receive = receive
        self.query_string = scope["query_string"].decode(ENCODING)
        self.raw_headers: Iterable[Tuple[bytes, bytes]] = scope["headers"]

    def get_headers(self) -> Dict[str, str]:
        return {header[0].decode(ENCODING): header[1].decode(ENCODING) for header in self.raw_headers}

    async def get_raw_body(self) -> str:
        chunks = bytearray()
        while True:
            chunk: Dict[str, Union[str, bytes]] = await self.receive()

            if chunk["type"] != "http.request":
                raise Exception("Body chunks could not be received from asgi server")

            chunks.extend(chunk.get("body", b""))
            if not chunk.get("more_body", False):
                break
        return bytes(chunks).decode(ENCODING)
