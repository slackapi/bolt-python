from typing import Iterable, Tuple

from asgiref.testing import ApplicationCommunicator

from slack_bolt.adapter.asgi.base_handler import BaseSlackRequestHandler

ENCODING = "utf-8"


class AsgiTestServerResponse:
    def __init__(
        self,
        status_code: int,
        headers: Iterable[Tuple[bytes, bytes]] = (),
        body: bytes = b"",
    ):
        self.status_code = status_code
        self._headers = headers
        self._body = body

    @property
    def body(self) -> str:
        return self._body.decode(ENCODING)

    @property
    def headers(self) -> dict:
        return {header[0].decode(ENCODING): header[1].decode(ENCODING) for header in self._headers}


class AsgiTestServerLifespanResponse:
    def __init__(self, type: str, message: str = ""):
        self.type = type
        self.message = message


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

    async def http(
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

        communicator = ApplicationCommunicator(self.asgi_app, scope)
        await communicator.send_input({"type": "http.request", "body": bytes(body, ENCODING), "more_body": False})

        response_start = await communicator.receive_output(timeout=1)
        response_body = await communicator.receive_output(timeout=1)

        return AsgiTestServerResponse(
            status_code=response_start["status"],
            headers=response_start.get("headers", []),
            body=response_body.get("body", b""),
        )

    async def lifespan(self, event: str) -> AsgiTestServerLifespanResponse:
        """This implements the server side behavior of the lifespan event
        https://asgi.readthedocs.io/en/latest/specs/lifespan.html

        Args:
            event (str): the lifespan type ex: "startup" for "lifespan.startup"
        """
        scope = dict(
            self.server_scope,
            **{
                "type": "lifespan",
            },
        )

        communicator = ApplicationCommunicator(self.asgi_app, scope)
        await communicator.send_input({"type": f"lifespan.{event}"})

        result = await communicator.receive_output(timeout=1)
        return AsgiTestServerLifespanResponse(
            type=result["type"],
            message=result.get("message", ""),
        )

    async def websocket(self) -> None:
        """This is not implemented"""
        scope = dict(
            self.server_scope,
            **{
                "type": "websocket",
            },
        )

        communicator = ApplicationCommunicator(self.asgi_app, scope)
        await communicator.send_input({})
        await communicator.receive_output(timeout=1)
