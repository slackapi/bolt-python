import asyncio
import json
import logging
import time
from http import client
from io import BytesIO
from multiprocessing import Process, Queue
from typing import Callable, List, Optional, Tuple
from unittest import TestCase
from urllib.error import URLError
from urllib.parse import ParseResult, parse_qs, urlparse
from urllib.request import urlopen
from wsgiref.headers import Headers

import bjoern

INVALID_AUTH = {
    "ok": False,
    "error": "invalid_auth",
}

OAUTH_V2_ACCESS_RESPONSE = json.dumps(
    {
        "ok": True,
        "access_token": "xoxb-17653672481-19874698323-pdFZKVeTuE8sk7oOcBrzbqgy",
        "token_type": "bot",
        "scope": "chat:write,commands",
        "bot_user_id": "U0KRQLJ9H",
        "app_id": "A0KRD7HC3",
        "team": {"name": "Slack Softball Team", "id": "T9TK3CUKW"},
        "enterprise": {"name": "slack-sports", "id": "E12345678"},
        "authed_user": {"id": "U1234", "scope": "chat:write", "access_token": "xoxp-1234", "token_type": "user"},
    }
)

OAUTH_V2_ACCESS_BOT_REFRESH_RESPONSE = json.dumps(
    {
        "ok": True,
        "app_id": "A0KRD7HC3",
        "access_token": "xoxb-valid-refreshed",
        "expires_in": 43200,
        "refresh_token": "xoxe-1-valid-bot-refreshed",
        "token_type": "bot",
        "scope": "chat:write,commands",
        "bot_user_id": "U0KRQLJ9H",
        "team": {"name": "Slack Softball Team", "id": "T9TK3CUKW"},
        "enterprise": {"name": "slack-sports", "id": "E12345678"},
    }
)

OAUTH_V2_ACCESS_USER_REFRESH_RESPONSE = json.dumps(
    {
        "ok": True,
        "app_id": "A0KRD7HC3",
        "access_token": "xoxp-valid-refreshed",
        "expires_in": 43200,
        "refresh_token": "xoxe-1-valid-user-refreshed",
        "token_type": "user",
        "scope": "search:read",
        "team": {"name": "Slack Softball Team", "id": "T9TK3CUKW"},
        "enterprise": {"name": "slack-sports", "id": "E12345678"},
    }
)
BOT_AUTH_TEST_RESPONSE = json.dumps(
    {
        "ok": True,
        "url": "https://subarachnoid.slack.com/",
        "team": "Subarachnoid Workspace",
        "user": "bot",
        "team_id": "T0G9PQBBK",
        "user_id": "W23456789",
        "bot_id": "BZYBOTHED",
    }
)

USER_AUTH_TEST_RESPONSE = json.dumps(
    {
        "ok": True,
        "url": "https://subarachnoid.slack.com/",
        "team": "Subarachnoid Workspace",
        "user": "some-user",
        "team_id": "T0G9PQBBK",
        "user_id": "W99999",
    }
)


class WsgiMockHandlerResponse:
    def __init__(self, status: int, headers: List[Tuple[str, str]], body: str):
        self.status = status
        self.headers = headers
        self.body = body

    @property
    def status_line(self) -> str:
        return f"{str(self.status)} {client.responses[self.status]}"


class WsgiMockHandlerRequest:
    def __init__(self, environ: dict):
        self.environ = environ

    def get_path(self) -> str:
        return self.environ["PATH_INFO"]

    def get_method(self) -> str:
        return self.environ["REQUEST_METHOD"]

    def get_content_length(self) -> int:
        return int(self.environ.get("CONTENT_LENGTH", 0))

    def get_header(self, header: str) -> str:
        key = header.replace("-", "_").upper()
        return self.environ[f"HTTP_{key}"]

    def body(self) -> BytesIO:
        try:
            return self.environ["wsgi.input"]
        except KeyError:
            return BytesIO()

    def parse_request_body(self, parsed_path: ParseResult) -> Optional[dict]:
        post_body = self.body().read(self.get_content_length())
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


class WsgiMockHandler:
    logger = logging.getLogger(__name__)

    def __init__(self, queue: Queue):
        self.queue = queue

    def is_valid_token(self, request: WsgiMockHandlerRequest):
        try:
            return request.get_header("Authorization").startswith("Bearer xoxb-")
        except KeyError:
            return False

    def is_valid_user_token(self, request: WsgiMockHandlerRequest):
        try:
            return request.get_header("Authorization").startswith("Bearer xoxp-")
        except KeyError:
            return False

    def _handle(self, request: WsgiMockHandlerRequest) -> WsgiMockHandlerResponse:
        parsed_path: ParseResult = urlparse(request.get_path())
        path = parsed_path.path
        self.queue.put(path)
        try:
            if path == "/health":
                return WsgiMockHandlerResponse(200, self.get_common_headers(), "OK")

            if path == "/webhook":
                return WsgiMockHandlerResponse(200, self.get_common_headers(), "OK")

            body = {"ok": True}
            if path == "/oauth.v2.access":
                if request.get_header("authorization") is not None:
                    request_body = request.parse_request_body(parsed_path=parsed_path)
                    # self.logger.info(f"request body: {request_body}")

                    if request_body.get("grant_type") == "refresh_token":
                        refresh_token = request_body.get("refresh_token")
                        if refresh_token is not None:
                            if "bot-valid" in refresh_token:
                                return WsgiMockHandlerResponse(
                                    200, self.get_common_headers(), OAUTH_V2_ACCESS_BOT_REFRESH_RESPONSE
                                )
                            if "user-valid" in refresh_token:
                                return WsgiMockHandlerResponse(
                                    200, self.get_common_headers(), OAUTH_V2_ACCESS_USER_REFRESH_RESPONSE
                                )
                    elif request_body.get("code") is not None:
                        return WsgiMockHandlerResponse(200, self.get_common_headers(), OAUTH_V2_ACCESS_RESPONSE)

            if self.is_valid_user_token(request):
                if path == "/auth.test":
                    return WsgiMockHandlerResponse(200, self.get_common_headers(), USER_AUTH_TEST_RESPONSE)

            if self.is_valid_token(request):
                if path == "/auth.test":
                    return WsgiMockHandlerResponse(200, self.get_common_headers(), BOT_AUTH_TEST_RESPONSE)

                request_body = request.parse_request_body(parsed_path=parsed_path)
                self.logger.info(f"request: {path} {request_body}")

                header = request.get_header("authorization")
                pattern = str(header).split("xoxb-", 1)[1]
                if pattern.isnumeric():
                    return WsgiMockHandlerResponse(int(pattern), self.get_common_headers(), """{"ok":false}""")
            else:
                body = INVALID_AUTH

            return WsgiMockHandlerResponse(200, self.get_common_headers(), json.dumps(body))

        except Exception as e:
            self.logger.error(str(e), exc_info=True)
            raise

    def get_common_headers(self, headers: List[Tuple[str, str]] = []) -> Headers:
        headers.append(("content-type", "application/json;charset=utf-8"))
        return headers

    def __call__(self, environ: dict, start_response: Callable):
        response = self._handle(WsgiMockHandlerRequest(environ))

        start_response(response.status_line, response.headers)
        return response.body.encode("utf-8")


def start_fake_server_thread(host: str, port: int, queue: Queue):
    handler = WsgiMockHandler(queue)
    bjoern.listen(handler, host, port)
    bjoern.run()


class MockReceivedRequests:
    def __init__(self, queue: Queue):
        self.queue = queue
        self.received_requests = {}

    def get(self, key, default=None):
        while not self.queue.empty():
            path = self.queue.get()
            self.received_requests[path] = self.received_requests.get(path, 0) + 1
        return self.received_requests.get(key, default)

    def __getitem__(self, item):
        while not self.queue.empty():
            path = self.queue.get()
            self.received_requests[path] = self.received_requests.get(path, 0) + 1
        return self.received_requests[item]


def setup_mock_web_api_server(test: TestCase):
    test.mock_received_requests = MockReceivedRequests(Queue())
    test.host = "127.0.0.1"
    test.port = 8888
    test.process = Process(target=start_fake_server_thread, args=(test.host, test.port, test.mock_received_requests.queue))
    test.process.start()
    wait_for_socket_mode_server(test.host, test.port, 5)


def wait_for_socket_mode_server(host: str, port: int, timeout: int):
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        try:
            urlopen(f"http://{host}:{port}/health")
            return
        except URLError:
            time.sleep(0.01)


def cleanup_mock_web_api_server(test: TestCase):
    test.mock_received_requests.queue.close()
    test.mock_received_requests.queue.join_thread()
    test.process.terminate()


def assert_auth_test_count(test: TestCase, expected_count: int):
    # time.sleep(0.01)
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
            # time.sleep(0.01)

    if error is not None:
        raise error


async def assert_auth_test_count_async(test: TestCase, expected_count: int):
    # await asyncio.sleep(0.01)
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
            await asyncio.sleep(0.01)

    if error is not None:
        raise error
