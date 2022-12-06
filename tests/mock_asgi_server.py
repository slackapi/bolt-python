from typing import Iterable, Tuple, Union
from slack_bolt.adapter.asgi.base_handler import BaseSlackRequestHandler

ENCODING = "latin-1"


class AsgiTestServerResponse:
    def __init__(self):
        self.status_code: int = None
        self._headers: Iterable[Tuple[bytes, bytes]] = []
        self._body: bytearray = bytearray(b"")

    @property
    def body(self):
        return self._body.decode(ENCODING)

    @property
    def headers(self):
        return {header[0].decode(ENCODING): header[1].decode(ENCODING) for header in self._headers}


class AsgiTestServer:
    def __init__(
        self,
        asgi_app: BaseSlackRequestHandler,
        root_path: str = "",
        scheme: str = "http",
        asgi: dict = {"version": "3.0", "spec_version": "2.3"},
        server: Tuple[str, int] = ("127.0.0.1", 4000),
    ):
        self.asgi_app = asgi_app
        self.server_scope = {"root_path": root_path, "scheme": scheme, "asgi": asgi, "server": server}

    async def http_request(
        self,
        method: str,
        headers: Iterable[Tuple[bytes, bytes]],
        body: str,
        path: str = "/slack/events",
        query_string: bytes = b"",
        http_version: str = "1.1",
        client: Tuple[str, int] = ("127.0.0.1", 60000),
    ) -> AsgiTestServerResponse:
        scope = dict(
            self.server_scope,
            **{
                "type": "http",
                "method": method,
                "headers": headers,
                "path": path,
                "raw_path": bytes(path, ENCODING),
                "query_string": query_string,
                "http_version": http_version,
                "client": client,
            },
        )

        async def receive():
            return {"type": "http.request", "body": bytes(body, ENCODING), "more_body": False}

        response = AsgiTestServerResponse()

        async def send(event):
            if event["type"] == "http.response.start":
                response.status_code = event["status"]
                response._headers = event["headers"]
            elif event["type"] == "http.response.body":
                response._body.extend(event["body"])
            else:
                raise TypeError(f"Sent type {event['type']} in response {event} is not valid")

        await self.asgi_app(scope, receive, send)
        return response
