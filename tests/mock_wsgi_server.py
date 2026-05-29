import io
from typing import Any, Callable, Dict, List, Optional, Tuple
from wsgiref.util import setup_testing_defaults
from wsgiref.validate import validator

from slack_bolt.adapter.wsgi import SlackRequestHandler

ENCODING = "utf-8"


class WsgiTestServerResponse:
    def __init__(self) -> None:
        self.status: Optional[str] = None
        self._headers: List[Tuple[str, str]] = []
        self._body: List[bytes] = []

    @property
    def headers(self) -> Dict[str, str]:
        return {header[0]: header[1] for header in self._headers}

    @property
    def body(self) -> str:
        return "".join([chunk.decode(ENCODING) for chunk in self._body])


class MockReadable:
    """PEP 3333 compliant input stream.

    Implements read, readline, readlines, and __iter__ as required
    by the WSGI specification for wsgi.input.
    """

    def __init__(self, body: str):
        self.body = body
        self._stream = io.BytesIO(bytes(body, ENCODING))

    def get_content_length(self) -> int:
        return len(self.body.encode(ENCODING))

    def read(self, size: int = -1) -> bytes:
        if size == -1:
            return self._stream.read()
        return self._stream.read(size)

    def readline(self, size: int = -1) -> bytes:
        if size == -1:
            return self._stream.readline()
        return self._stream.readline(size)

    def readlines(self, hint: int = -1) -> List[bytes]:
        return self._stream.readlines(hint)

    def __iter__(self):
        return iter(self._stream)


class WsgiTestServer:
    def __init__(
        self,
        wsgi_app: SlackRequestHandler,
        root_path: str = "",
        input_terminated: bool = True,
        server_software: str = "mock/0.0.0",
        url_scheme: str = "https",
        remote_addr: str = "127.0.0.1",
        remote_port: str = "63263",
    ):
        self.root_path = root_path
        self.wsgi_app = validator(wsgi_app)
        self.environ: Dict[str, Any] = {}
        setup_testing_defaults(self.environ)
        self.environ.update(
            {
                "wsgi.input_terminated": input_terminated,
                "wsgi.errors": io.StringIO(),
                "SERVER_SOFTWARE": server_software,
                "wsgi.url_scheme": url_scheme,
                "REMOTE_ADDR": remote_addr,
                "REMOTE_PORT": remote_port,
            }
        )

    def http(
        self,
        method: str,
        headers: Dict[str, str],
        body: Optional[str] = None,
        path: str = "/slack/events",
        query_string: str = "",
        server_protocol: str = "HTTP/1.1",
        server_name: str = "0.0.0.0",
        server_port: str = "3000",
        script_name: str = "",
    ) -> WsgiTestServerResponse:
        environ = dict(
            self.environ,
            **{
                "REQUEST_METHOD": method,
                "PATH_INFO": f"{self.root_path}{path}",
                "QUERY_STRING": query_string,
                "RAW_URI": f"{self.root_path}{path}?{query_string}",
                "SERVER_PROTOCOL": server_protocol,
                "SERVER_NAME": server_name,
                "SERVER_PORT": server_port,
                "SCRIPT_NAME": script_name,
            },
        )
        for key, value in headers.items():
            header_key = key.upper().replace("-", "_")
            if header_key in {"CONTENT_LENGTH", "CONTENT_TYPE"}:
                environ[header_key] = value
            else:
                environ[f"HTTP_{header_key}"] = value

        if body is not None:
            readable = MockReadable(body)
            environ["wsgi.input"] = readable
            if "CONTENT_LENGTH" not in environ:
                environ["CONTENT_LENGTH"] = str(readable.get_content_length())
        else:
            environ["wsgi.input"] = MockReadable("")

        response = WsgiTestServerResponse()

        def start_response(
            status: str,
            headers: List[Tuple[str, str]],
            exc_info: Optional[Any] = None,
        ) -> Callable[[bytes], object]:
            response.status = status
            response._headers = headers
            return lambda s: None

        iterator = self.wsgi_app(environ, start_response)
        try:
            response._body = list(iterator)
        finally:
            if hasattr(iterator, "close"):
                iterator.close()

        return response
