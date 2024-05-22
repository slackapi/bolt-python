from typing import Any, Callable, Dict, Union

from .utils import ENCODING


class WsgiHttpRequest:
    __slots__ = ("receive", "query_string", "raw_headers")

    def __init__(self,  environ: Dict[str, Any]):
        self.receive = environ["wsgi.input"]
        self.query_string = str(environ["QUERY_STRING"], ENCODING)
        self.environ = environ

    def get_headers(self) -> Dict[str, str]:
        headers = {}
        for e in self.environ:
            if e[0].startswith("HTTP_"):
                key = e[0][len("HTTP_"):].lower().replace("_", "-")
                headers[key] = e[1]
        return headers

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
