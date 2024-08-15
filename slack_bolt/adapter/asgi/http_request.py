from typing import Callable, Dict, Iterable, Sequence, Tuple, Union

from .utils import scope_type, ENCODING


class AsgiHttpRequest:
    __slots__ = ("receive", "query_string", "raw_headers")

    def __init__(self, scope: scope_type, receive: Callable):
        self.receive = receive
        self.query_string = str(scope["query_string"], ENCODING)  # type: ignore[arg-type]
        self.raw_headers: Iterable[Tuple[bytes, bytes]] = scope["headers"]  # type: ignore[assignment]

    def get_headers(self) -> Dict[str, Union[str, Sequence[str]]]:
        return {str(header[0], ENCODING): str(header[1], (ENCODING)) for header in self.raw_headers}

    async def get_raw_body(self) -> str:
        chunks = bytearray()
        while True:
            chunk: Dict[str, Union[str, bytes]] = await self.receive()

            if chunk["type"] != "http.request":
                raise Exception("Body chunks could not be received from asgi server")

            chunks.extend(chunk.get("body", b""))  # type: ignore[arg-type]
            if not chunk.get("more_body", False):
                break
        return bytes(chunks).decode(ENCODING)
