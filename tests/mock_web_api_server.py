import asyncio
import json
import logging
from queue import Queue
import threading
import time
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Type, Optional
from unittest import TestCase
from urllib.parse import urlparse, parse_qs, ParseResult


class MockHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    default_request_version = "HTTP/1.1"
    logger = logging.getLogger(__name__)
    received_requests = {}

    def is_valid_token(self):
        return "Authorization" in self.headers and str(self.headers["Authorization"]).startswith("Bearer xoxb-")

    def is_valid_user_token(self):
        return "Authorization" in self.headers and str(self.headers["Authorization"]).startswith("Bearer xoxp-")

    def set_common_headers(self, content_length: int = 0):
        self.send_header("content-type", "application/json;charset=utf-8")
        self.send_header("Content-Length", str(content_length))
        self.end_headers()

    invalid_auth = {
        "ok": False,
        "error": "invalid_auth",
    }

    oauth_v2_access_response = """
{
    "ok": true,
    "access_token": "xoxb-17653672481-19874698323-pdFZKVeTuE8sk7oOcBrzbqgy",
    "token_type": "bot",
    "scope": "chat:write,commands",
    "bot_user_id": "U0KRQLJ9H",
    "app_id": "A0KRD7HC3",
    "team": {
        "name": "Slack Softball Team",
        "id": "T9TK3CUKW"
    },
    "enterprise": {
        "name": "slack-sports",
        "id": "E12345678"
    },
    "authed_user": {
        "id": "U1234",
        "scope": "chat:write",
        "access_token": "xoxp-1234",
        "token_type": "user"
    }
}
"""
    oauth_v2_access_bot_refresh_response = """
    {
        "ok": true,
        "app_id": "A0KRD7HC3",
        "access_token": "xoxb-valid-refreshed",
        "expires_in": 43200,
        "refresh_token": "xoxe-1-valid-bot-refreshed",
        "token_type": "bot",
        "scope": "chat:write,commands",
        "bot_user_id": "U0KRQLJ9H",
        "team": {
            "name": "Slack Softball Team",
            "id": "T9TK3CUKW"
        },
        "enterprise": {
            "name": "slack-sports",
            "id": "E12345678"
        }
    }
"""
    oauth_v2_access_user_refresh_response = """
        {
            "ok": true,
            "app_id": "A0KRD7HC3",
            "access_token": "xoxp-valid-refreshed",
            "expires_in": 43200,
            "refresh_token": "xoxe-1-valid-user-refreshed",
            "token_type": "user",
            "scope": "search:read",
            "team": {
                "name": "Slack Softball Team",
                "id": "T9TK3CUKW"
            },
            "enterprise": {
                "name": "slack-sports",
                "id": "E12345678"
            }
        }
    """
    bot_auth_test_response = """
{
    "ok": true,
    "url": "https://subarachnoid.slack.com/",
    "team": "Subarachnoid Workspace",
    "user": "bot",
    "team_id": "T0G9PQBBK",
    "user_id": "W23456789",
    "bot_id": "BZYBOTHED"
}
"""

    user_auth_test_response = """
{
    "ok": true,
    "url": "https://subarachnoid.slack.com/",
    "team": "Subarachnoid Workspace",
    "user": "some-user",
    "team_id": "T0G9PQBBK",
    "user_id": "W99999"
}
"""

    def _handle(self):
        parsed_path: ParseResult = urlparse(self.path)
        path = parsed_path.path
        self.server.queue.put(path)
        self.received_requests[path] = self.received_requests.get(path, 0) + 1
        try:
            if path == "/webhook":
                self.send_response(200)
                self.set_common_headers(len("OK"))
                self.wfile.write("OK".encode("utf-8"))
                return

            body = {"ok": True}
            if path == "/oauth.v2.access":
                if self.headers.get("authorization") is not None:
                    request_body = self._parse_request_body(
                        parsed_path=parsed_path,
                        content_len=int(self.headers.get("Content-Length") or 0),
                    )
                    self.logger.info(f"request body: {request_body}")

                    if request_body.get("grant_type") == "refresh_token":
                        refresh_token = request_body.get("refresh_token")
                        if refresh_token is not None:
                            if "bot-valid" in refresh_token:
                                self.send_response(200)
                                self.set_common_headers(len(self.oauth_v2_access_bot_refresh_response))
                                body = self.oauth_v2_access_bot_refresh_response
                                self.wfile.write(body.encode("utf-8"))
                                return
                            if "user-valid" in refresh_token:
                                self.send_response(200)
                                self.set_common_headers(len(self.oauth_v2_access_user_refresh_response))
                                body = self.oauth_v2_access_user_refresh_response
                                self.wfile.write(body.encode("utf-8"))
                                return
                    elif request_body.get("code") is not None:
                        self.send_response(200)
                        self.set_common_headers(len(self.oauth_v2_access_response))
                        self.wfile.write(self.oauth_v2_access_response.encode("utf-8"))
                        return

            if self.is_valid_user_token():
                if path == "/auth.test":
                    self.send_response(200)
                    self.set_common_headers(len(self.user_auth_test_response))
                    self.wfile.write(self.user_auth_test_response.encode("utf-8"))
                    return

            if self.is_valid_token():
                if path == "/auth.test":
                    self.send_response(200)
                    self.set_common_headers(len(self.bot_auth_test_response))
                    self.wfile.write(self.bot_auth_test_response.encode("utf-8"))
                    return

                request_body = self._parse_request_body(
                    parsed_path=parsed_path,
                    content_len=int(self.headers.get("Content-Length") or 0),
                )
                self.logger.info(f"request: {path} {request_body}")

                header = self.headers["authorization"]
                pattern = str(header).split("xoxb-", 1)[1]
                if pattern.isnumeric():
                    ok_false_body = """{"ok":false}"""
                    self.send_response(int(pattern))
                    self.set_common_headers(len(ok_false_body))
                    self.wfile.write(ok_false_body.encode("utf-8"))
                    return
            else:
                body = self.invalid_auth

            self.send_response(HTTPStatus.OK)
            self.set_common_headers(len(json.dumps(body)))
            self.wfile.write(json.dumps(body).encode("utf-8"))

        except Exception as e:
            self.logger.error(str(e), exc_info=True)
            raise

    def do_GET(self):
        self._handle()

    def do_POST(self):
        self._handle()

    def _parse_request_body(self, parsed_path: str, content_len: int) -> Optional[dict]:
        post_body = self.rfile.read(content_len)
        request_body = None
        if post_body:
            try:
                post_body = post_body.decode("utf-8")
                if post_body.startswith("{"):
                    request_body = json.loads(post_body)
                else:
                    request_body = {k: v[0] for k, v in parse_qs(post_body).items()}
            except UnicodeDecodeError:
                pass
        else:
            if parsed_path and parsed_path.query:
                request_body = {k: v[0] for k, v in parse_qs(parsed_path.query).items()}
        return request_body


class MockServerThread(threading.Thread):
    def __init__(self, queue: Queue, test: TestCase, handler: Type[SimpleHTTPRequestHandler] = MockHandler):
        threading.Thread.__init__(self)
        self.handler = handler
        self.test = test
        self.queue = queue

    def run(self):
        self.server = HTTPServer(("localhost", 8888), self.handler)
        self.server.queue = self.queue
        self.test.mock_received_requests = self.handler.received_requests
        self.test.server_url = "http://localhost:8888"
        self.test.host, self.test.port = self.server.socket.getsockname()
        self.test.server_started.set()  # threading.Event()

        self.test = None
        try:
            self.server.serve_forever(0.05)
        finally:
            self.server.server_close()

    def stop(self):
        self.handler.received_requests = {}
        self.server.shutdown()
        self.join()


class ReceivedRequestsHandler:
    def __init__(self, queue: Queue):
        self.queue = queue
        self.received_requests = {}

    def get(self, key, default=None):
        while not self.queue.empty():
            path = self.queue.get()
            self.received_requests[path] = self.received_requests.get(path, 0) + 1
        return self.received_requests.get(key, default)


def setup_mock_web_api_server(test: TestCase):
    test.server_started = threading.Event()
    test.received_requests_handler = ReceivedRequestsHandler(Queue())
    test.thread = MockServerThread(test.received_requests_handler.queue, test)
    test.thread.start()
    test.server_started.wait()


def cleanup_mock_web_api_server(test: TestCase):
    test.thread.stop()
    test.thread = None


def assert_received_request_count(test: TestCase, path: str, min_count: int, timeout: float = 1):
    start_time = time.time()
    error = None
    while time.time() - start_time < timeout:
        try:
            assert test.received_requests_handler.get(path, 0) == min_count
            return
        except Exception as e:
            error = e
            # waiting for mock_received_requests updates
            time.sleep(0.05)

    if error is not None:
        raise error


def assert_auth_test_count(test: TestCase, expected_count: int):
    assert_received_request_count(test, "/auth.test", expected_count, 0.5)


async def assert_auth_test_count_async(test: TestCase, expected_count: int):
    await asyncio.sleep(0.1)
    retry_count = 0
    error = None
    while retry_count < 3:
        try:
            test.mock_received_requests.get("/auth.test", 0) == expected_count
            break
        except Exception as e:
            error = e
            retry_count += 1
            # waiting for mock_received_requests updates
            await asyncio.sleep(0.1)

    if error is not None:
        raise error
