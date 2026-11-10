import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qsl

from slack_sdk import WebClient

DEFAULT_TEAM_ID = "T0000000000"
DEFAULT_USER_ID = "U0000000000"
DEFAULT_BOT_USER_ID = "U00000000BT"
DEFAULT_BOT_ID = "B0000000000"
DEFAULT_APP_ID = "A0000000000"


class APICall:
    """A Web API call received by `MockSlackServer`."""

    method: str
    """The API method name, e.g. `chat.postMessage`."""
    args: Dict[str, Any]
    """The arguments sent with the call, parsed from the JSON or form body."""
    headers: Dict[str, str]
    """The request headers."""

    def __init__(self, *, method: str, args: Dict[str, Any], headers: Dict[str, str]):
        self.method = method
        self.args = args
        self.headers = headers

    @property
    def token(self) -> Optional[str]:
        """The token sent in the Authorization header, if any."""
        auth = self.headers.get("authorization") or ""
        return auth[len("Bearer ") :] if auth.startswith("Bearer ") else None

    def __repr__(self) -> str:
        return f"APICall(method={self.method!r}, args={self.args!r})"


class MockSlackServer:
    """An in-process stand-in for the Slack Web API and `response_url` endpoints, for tests.

    It records every Web API call and every message posted to a `response_url`, and answers
    them with canned responses. `auth.test` is answered with a bot installation by default,
    and any other method returns `{"ok": true}` unless a response is set with `set_response()`.

        server = MockSlackServer()
        server.start()
        app = App(client=server.web_client("xoxb-test"), signing_secret="secret")
        ...
        server.stop()

    It can also be used as a context manager, which starts and stops the server.
    """

    def __init__(
        self,
        *,
        team_id: str = DEFAULT_TEAM_ID,
        bot_user_id: str = DEFAULT_BOT_USER_ID,
        bot_id: str = DEFAULT_BOT_ID,
        responses: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        self.team_id = team_id
        self.bot_user_id = bot_user_id
        self.bot_id = bot_id
        self._responses: Dict[str, Dict[str, Any]] = dict(responses or {})
        self._calls: List[APICall] = []
        self._responds: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self._server: Optional[ThreadingHTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    # -------------------------
    # lifecycle

    def start(self) -> "MockSlackServer":
        if self._server is not None:
            return self
        handler = _build_handler(self)
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self._server.daemon_threads = True
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self

    def stop(self) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def __enter__(self) -> "MockSlackServer":
        return self.start()

    def __exit__(self, *args) -> None:
        self.stop()

    # -------------------------
    # urls and clients

    @property
    def url(self) -> str:
        if self._server is None:
            raise RuntimeError("MockSlackServer is not running. Call start() first.")
        port = self._server.server_address[1]
        return f"http://127.0.0.1:{port}"

    @property
    def base_url(self) -> str:
        """The Web API base URL to pass to `WebClient(base_url=...)`."""
        return f"{self.url}/api/"

    def response_url(self, path: str = "T0000000000/1/test") -> str:
        """A `response_url` that records the messages posted to it."""
        return f"{self.url}/response_url/{path}"

    def web_client(self, token: Optional[str] = "xoxb-test-token") -> WebClient:
        """A `WebClient` that sends its requests to this server."""
        return WebClient(token=token, base_url=self.base_url)

    # -------------------------
    # recorded requests

    @property
    def calls(self) -> List[APICall]:
        """All Web API calls received, in order."""
        with self._lock:
            return list(self._calls)

    def calls_to(self, method: str) -> List[APICall]:
        """The Web API calls received for the given method, e.g. `chat.postMessage`."""
        return [c for c in self.calls if c.method == method]

    @property
    def responds(self) -> List[Dict[str, Any]]:
        """The message bodies posted to `response_url`s (e.g. by `respond()`), in order."""
        with self._lock:
            return list(self._responds)

    def set_response(self, method: str, body: Dict[str, Any]) -> None:
        """Sets the response body returned for the given Web API method."""
        with self._lock:
            self._responses[method] = body

    def reset(self) -> None:
        """Clears the recorded calls and responds. Canned responses are kept."""
        with self._lock:
            self._calls.clear()
            self._responds.clear()

    # -------------------------
    # internals

    def _response_for(self, method: str) -> Dict[str, Any]:
        with self._lock:
            if method in self._responses:
                return self._responses[method]
        if method == "auth.test":
            return {
                "ok": True,
                "url": "https://test.slack.com/",
                "team": "Test Workspace",
                "user": "bot",
                "team_id": self.team_id,
                "user_id": self.bot_user_id,
                "bot_id": self.bot_id,
                "is_enterprise_install": False,
            }
        return {"ok": True}

    def _record_call(self, call: APICall) -> None:
        with self._lock:
            self._calls.append(call)

    def _record_respond(self, body: Dict[str, Any]) -> None:
        with self._lock:
            self._responds.append(body)


def _parse_body(raw: bytes, content_type: str) -> Dict[str, Any]:
    if not raw:
        return {}
    text = raw.decode("utf-8")
    if "application/json" in content_type:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {"body": parsed}
    if "application/x-www-form-urlencoded" in content_type:
        return dict(parse_qsl(text, keep_blank_values=True))
    return {"body": text}


def _build_handler(server: MockSlackServer):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):  # silence the default stderr logging
            pass

        def _read(self) -> Dict[str, Any]:
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""
            args = _parse_body(raw, self.headers.get("Content-Type") or "")
            query = self.path.split("?", 1)[1] if "?" in self.path else ""
            if query:
                args = {**dict(parse_qsl(query, keep_blank_values=True)), **args}
            return args

        def _send(self, status: int, body: Dict[str, Any]) -> None:
            data = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json;charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _handle(self) -> None:
            path = self.path.split("?", 1)[0]
            if path.startswith("/api/"):
                method = path[len("/api/") :]
                headers = {k.lower(): v for k, v in self.headers.items()}
                server._record_call(APICall(method=method, args=self._read(), headers=headers))
                self._send(200, server._response_for(method))
            elif path.startswith("/response_url/"):
                server._record_respond(self._read())
                self._send(200, {"ok": True})
            else:
                self._send(404, {"ok": False, "error": "not_found"})

        def do_POST(self):
            self._handle()

        def do_GET(self):
            self._handle()

    return Handler
