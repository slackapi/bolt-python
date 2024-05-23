from typing import Dict, Iterable, Optional, Tuple
from slack_bolt.adapter.wsgi import SlackRequestHandler

ENCODING = "utf-8"


class WsgiTestServerResponse:
    def __init__(self):
        self.status: int = None
        self._headers: Iterable[Tuple[str, str]] = []
        self._body: Iterable[bytes] = []

    @property
    def headers(self):
        return {header[0]: header[1] for header in self.headers}

    @property
    def body(self, length: int):
        return "".join([chunk.decode(ENCODING) for chunk in self._body[length:]])


class WsgiTestServer:
    def __init__(
        self,
        wsgi_app: SlackRequestHandler,
        root_path: str = "",
        version: Tuple[int, int] = (1, 0),
        multithread: bool = False,
        multiprocess: bool = False,
        run_once: bool = False,
        input_terminated: bool = True,
        server_software: bool = "mock/0.0.0",
        url_scheme: str = "https",
        remote_addr: str = "127.0.0.1",
        remote_port: str = "63263",
        server_name: str = "0.0.0.0",
        server_port: str = "3000",
        script_name: str = "",
    ):
        self.root_path = root_path
        self.wsgi_app = wsgi_app
        self.environ = {
            "wsgi.version": version,
            "wsgi.multithread": multithread,
            "wsgi.multiprocess": multiprocess,
            "wsgi.run_once": run_once,
            "wsgi.input_terminated": input_terminated,
            "SERVER_SOFTWARE": server_software,
            "wsgi.url_scheme": url_scheme,
            "REMOTE_ADDR": remote_addr,
            "REMOTE_PORT": remote_port,
            "SERVER_NAME": server_name,
            "SERVER_PORT": server_port,
            "SCRIPT_NAME": script_name,
        }

    async def http(
        self,
        method: str,
        headers: Dict[str, str],
        body: Optional[str],
        path: str = "/slack/events",
        query_string: str = "",
        server_protocol: str = "HTTP/1.1",
    ) -> WsgiTestServerResponse:
        environ = dict(
            self.environ,
            **{
                "wsgi.input": "something to read",
                "REQUEST_METHOD": method,
                "PATH_INFO": f"{self.root_path}{path}",
                "QUERY_STRING": query_string,
                "RAW_URI": f"{self.root_path}{path}?{query_string}",
                "SERVER_PROTOCOL": server_protocol,
            },
        )
        for key, value in headers.items():
            header_key = key.upper().replace("-", "_")
            if header_key in {"CONTENT_LENGTH", "CONTENT_TYPE"}:
                environ[header_key] = value
            else:
                environ[f"HTTP_{header_key}"] = value
        
        class MockReadable():
            def __init__(self, body: str):
                self.body = body
                self._body = bytes(body, ENCODING)

            def get_content_length(self) -> int:
                return len(self._body)

            def read(self, length) -> bytes:
                return self._body[length:]
        
        if body is not None:
            environ["wsgi.input"] = MockReadable(body)
            if "CONTENT_LENGTH" not in environ:
                environ["CONTENT_LENGTH"] = str(environ["wsgi.input"].get_content_length())

        response = WsgiTestServerResponse()

        def start_response(status, headers):
            response.status = status,
            response.headers = headers

        response.body = self.wsgi_app(environ=environ, start_response=start_response)

        return response
