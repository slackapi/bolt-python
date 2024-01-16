import asyncio
from io import BytesIO
import json
import logging
import threading
import time
from http.client import responses
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Callable, Dict, List, Tuple, Type, Optional
from unittest import TestCase
from urllib import request
from urllib.error import URLError
from urllib.parse import urlparse, parse_qs, ParseResult
from urllib.request import urlopen
from wsgiref.headers import Headers
import bjoern
from multiprocessing import Process


# class MockHandler(SimpleHTTPRequestHandler):
#     protocol_version = "HTTP/1.1"
#     default_request_version = "HTTP/1.1"
#     logger = logging.getLogger(__name__)
#     received_requests = {}

#     def is_valid_token(self):
#         return "Authorization" in self.headers and str(self.headers["Authorization"]).startswith("Bearer xoxb-")

#     def is_valid_user_token(self):
#         return "Authorization" in self.headers and str(self.headers["Authorization"]).startswith("Bearer xoxp-")

#     def set_common_headers(self):
#         self.send_header("content-type", "application/json;charset=utf-8")
#         self.send_header("connection", "close")
#         self.end_headers()

#     invalid_auth = {
#         "ok": False,
#         "error": "invalid_auth",
#     }

#     oauth_v2_access_response = """
# {
#     "ok": true,
#     "access_token": "xoxb-17653672481-19874698323-pdFZKVeTuE8sk7oOcBrzbqgy",
#     "token_type": "bot",
#     "scope": "chat:write,commands",
#     "bot_user_id": "U0KRQLJ9H",
#     "app_id": "A0KRD7HC3",
#     "team": {
#         "name": "Slack Softball Team",
#         "id": "T9TK3CUKW"
#     },
#     "enterprise": {
#         "name": "slack-sports",
#         "id": "E12345678"
#     },
#     "authed_user": {
#         "id": "U1234",
#         "scope": "chat:write",
#         "access_token": "xoxp-1234",
#         "token_type": "user"
#     }
# }
# """
#     oauth_v2_access_bot_refresh_response = """
#     {
#         "ok": true,
#         "app_id": "A0KRD7HC3",
#         "access_token": "xoxb-valid-refreshed",
#         "expires_in": 43200,
#         "refresh_token": "xoxe-1-valid-bot-refreshed",
#         "token_type": "bot",
#         "scope": "chat:write,commands",
#         "bot_user_id": "U0KRQLJ9H",
#         "team": {
#             "name": "Slack Softball Team",
#             "id": "T9TK3CUKW"
#         },
#         "enterprise": {
#             "name": "slack-sports",
#             "id": "E12345678"
#         }
#     }
# """
#     oauth_v2_access_user_refresh_response = """
#         {
#             "ok": true,
#             "app_id": "A0KRD7HC3",
#             "access_token": "xoxp-valid-refreshed",
#             "expires_in": 43200,
#             "refresh_token": "xoxe-1-valid-user-refreshed",
#             "token_type": "user",
#             "scope": "search:read",
#             "team": {
#                 "name": "Slack Softball Team",
#                 "id": "T9TK3CUKW"
#             },
#             "enterprise": {
#                 "name": "slack-sports",
#                 "id": "E12345678"
#             }
#         }
#     """
#     bot_auth_test_response = """
# {
#     "ok": true,
#     "url": "https://subarachnoid.slack.com/",
#     "team": "Subarachnoid Workspace",
#     "user": "bot",
#     "team_id": "T0G9PQBBK",
#     "user_id": "W23456789",
#     "bot_id": "BZYBOTHED"
# }
# """

#     user_auth_test_response = """
# {
#     "ok": true,
#     "url": "https://subarachnoid.slack.com/",
#     "team": "Subarachnoid Workspace",
#     "user": "some-user",
#     "team_id": "T0G9PQBBK",
#     "user_id": "W99999"
# }
# """

#     def _handle(self):
#         parsed_path: ParseResult = urlparse(self.path)
#         path = parsed_path.path
#         self.received_requests[path] = self.received_requests.get(path, 0) + 1
#         try:
#             if path == "/webhook":
#                 self.send_response(200)
#                 self.set_common_headers()
#                 self.wfile.write("OK".encode("utf-8"))
#                 return

#             if path == "/received_requests.json":
#                 self.send_response(200)
#                 self.set_common_headers()
#                 self.wfile.write(json.dumps(self.received_requests).encode("utf-8"))
#                 return

#             body = {"ok": True}
#             if path == "/oauth.v2.access":
#                 if self.headers.get("authorization") is not None:
#                     request_body = self._parse_request_body(
#                         parsed_path=parsed_path,
#                         content_len=int(self.headers.get("Content-Length") or 0),
#                     )
#                     self.logger.info(f"request body: {request_body}")

#                     if request_body.get("grant_type") == "refresh_token":
#                         refresh_token = request_body.get("refresh_token")
#                         if refresh_token is not None:
#                             if "bot-valid" in refresh_token:
#                                 self.send_response(200)
#                                 self.set_common_headers()
#                                 body = self.oauth_v2_access_bot_refresh_response
#                                 self.wfile.write(body.encode("utf-8"))
#                                 return
#                             if "user-valid" in refresh_token:
#                                 self.send_response(200)
#                                 self.set_common_headers()
#                                 body = self.oauth_v2_access_user_refresh_response
#                                 self.wfile.write(body.encode("utf-8"))
#                                 return
#                     elif request_body.get("code") is not None:
#                         self.send_response(200)
#                         self.set_common_headers()
#                         self.wfile.write(self.oauth_v2_access_response.encode("utf-8"))
#                         return

#             if self.is_valid_user_token():
#                 if path == "/auth.test":
#                     self.send_response(200)
#                     self.set_common_headers()
#                     self.wfile.write(self.user_auth_test_response.encode("utf-8"))
#                     return

#             if self.is_valid_token():
#                 if path == "/auth.test":
#                     self.send_response(200)
#                     self.set_common_headers()
#                     self.wfile.write(self.bot_auth_test_response.encode("utf-8"))
#                     return

#                 request_body = self._parse_request_body(
#                     parsed_path=parsed_path,
#                     content_len=int(self.headers.get("Content-Length") or 0),
#                 )
#                 self.logger.info(f"request: {path} {request_body}")

#                 header = self.headers["authorization"]
#                 pattern = str(header).split("xoxb-", 1)[1]
#                 if pattern.isnumeric():
#                     self.send_response(int(pattern))
#                     self.set_common_headers()
#                     self.wfile.write("""{"ok":false}""".encode("utf-8"))
#                     return
#             else:
#                 body = self.invalid_auth

#             self.send_response(HTTPStatus.OK)
#             self.set_common_headers()
#             self.wfile.write(json.dumps(body).encode("utf-8"))
#             self.wfile.close()

#         except Exception as e:
#             self.logger.error(str(e), exc_info=True)
#             raise

#     def do_GET(self):
#         self._handle()

#     def do_POST(self):
#         self._handle()

#     def _parse_request_body(self, parsed_path: str, content_len: int) -> Optional[dict]:
#         post_body = self.rfile.read(content_len)
#         request_body = None
#         if post_body:
#             try:
#                 post_body = post_body.decode("utf-8")
#                 if post_body.startswith("{"):
#                     request_body = json.loads(post_body)
#                 else:
#                     request_body = {k: v[0] for k, v in parse_qs(post_body).items()}
#             except UnicodeDecodeError:
#                 pass
#         else:
#             if parsed_path and parsed_path.query:
#                 request_body = {k: v[0] for k, v in parse_qs(parsed_path.query).items()}
#         return request_body


class FakeWSGIResponse:
    def __init__(self, status: int, headers: List[Tuple[str, str]], body: str):
        self.status = status
        self.headers = headers
        self.body = body

    @property
    def status_line(self) -> str:
        return f"{str(self.status)} {responses[self.status]}"


class WSGIEnviron:
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


class MockWSGIHandler:
    logger = logging.getLogger(__name__)

    received_requests: Dict[str, int] = {}

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

    def is_valid_token(self, environ: WSGIEnviron):
        try:
            return environ.get_header("Authorization").startswith("Bearer xoxb-")
        except KeyError:
            return False

    def is_valid_user_token(self, environ: WSGIEnviron):
        try:
            return environ.get_header("Authorization").startswith("Bearer xoxp-")
        except KeyError:
            return False

    def _handle(self, environ: WSGIEnviron) -> FakeWSGIResponse:
        parsed_path: ParseResult = urlparse(environ.get_path())
        path = parsed_path.path
        self.received_requests[path] = self.received_requests.get(path, 0) + 1
        try:
            if path == "/health":
                return FakeWSGIResponse(200, self.get_common_headers(), "OK")

            if path == "/webhook":
                return FakeWSGIResponse(200, self.get_common_headers(), "OK")

            if path == "/received_requests.json":
                return FakeWSGIResponse(200, self.get_common_headers(), json.dumps(self.received_requests))

            body = {"ok": True}
            if path == "/oauth.v2.access":
                if environ.get_header("authorization") is not None:
                    request_body = self._parse_request_body(
                        parsed_path=parsed_path,
                        body=environ.body(),
                        content_len=environ.get_content_length(),
                    )
                    # self.logger.info(f"request body: {request_body}")

                    if request_body.get("grant_type") == "refresh_token":
                        refresh_token = request_body.get("refresh_token")
                        if refresh_token is not None:
                            if "bot-valid" in refresh_token:
                                return FakeWSGIResponse(
                                    200, self.get_common_headers(), self.oauth_v2_access_bot_refresh_response
                                )
                            if "user-valid" in refresh_token:
                                return FakeWSGIResponse(
                                    200, self.get_common_headers(), self.oauth_v2_access_user_refresh_response
                                )
                    elif request_body.get("code") is not None:
                        return FakeWSGIResponse(200, self.get_common_headers(), self.oauth_v2_access_response)

            if self.is_valid_user_token(environ):
                if path == "/auth.test":
                    return FakeWSGIResponse(200, self.get_common_headers(), self.user_auth_test_response)

            if self.is_valid_token(environ):
                if path == "/auth.test":
                    return FakeWSGIResponse(200, self.get_common_headers(), self.bot_auth_test_response)

                request_body = self._parse_request_body(
                    parsed_path=parsed_path,
                    body=environ.body(),
                    content_len=environ.get_content_length(),
                )
                self.logger.info(f"request: {path} {request_body}")

                header = environ.get_header("authorization")
                pattern = str(header).split("xoxb-", 1)[1]
                if pattern.isnumeric():
                    return FakeWSGIResponse(int(pattern), self.get_common_headers(), """{"ok":false}""")
            else:
                body = self.invalid_auth

            return FakeWSGIResponse(200, self.get_common_headers(), json.dumps(body))

        except Exception as e:
            self.logger.error(str(e), exc_info=True)
            raise

    def _parse_request_body(self, parsed_path: str, body: BytesIO, content_len: int) -> Optional[dict]:
        post_body = body.read(content_len)
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

    def get_common_headers(self, headers: List[Tuple[str, str]] = []) -> Headers:
        headers.append(("content-type", "application/json;charset=utf-8"))
        headers.append(("connection", "close"))
        return headers

    def __call__(self, environ: dict, start_response: Callable):
        response = self._handle(WSGIEnviron(environ))

        start_response(response.status_line, response.headers)
        return response.body.encode("utf-8")


def start_fake_server_thread(test: TestCase, port: int):
    test.handler = MockWSGIHandler()
    test.socket = bjoern.listen(test.handler, "127.0.0.1", port)
    test.host, test.port = test.socket.getsockname()

    bjoern.run()


class MockReceivedRequests:
    def get(self, key, default=None):
        url = "http://127.0.0.1:8888/received_requests.json"
        r = urlopen(url)
        data: dict = json.loads(r.read().decode(r.info().get_param("charset") or "utf-8"))
        return data.get(key, default)

    def __getitem__(self, item):
        url = "http://127.0.0.1:8888/received_requests.json"
        r = urlopen(url)
        data = json.loads(r.read().decode(r.info().get_param("charset") or "utf-8"))
        return data[item]


def setup_mock_web_api_server(test: TestCase):
    test.thread = Process(target=start_fake_server_thread, args=(test, 8888))
    test.thread.start()
    test.thread.pid
    test.mock_received_requests = MockReceivedRequests()
    wait_for_socket_mode_server(8888, 5)


def wait_for_socket_mode_server(port: int, timeout: int):
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        try:
            urlopen(f"http://127.0.0.1:{port}/health")
            return
        except URLError:
            time.sleep(0.01)


def cleanup_mock_web_api_server(test: TestCase):
    test.thread.kill()


def assert_auth_test_count(test: TestCase, expected_count: int):
    time.sleep(0.1)
    retry_count = 0
    error = None
    while retry_count < 3:
        try:
            received_requests = MockReceivedRequests()
            received_requests["/auth.test"] == expected_count
            break
        except Exception as e:
            error = e
            retry_count += 1
            # waiting for mock_received_requests updates
            time.sleep(0.1)

    if error is not None:
        raise error


async def assert_auth_test_count_async(test: TestCase, expected_count: int):
    await asyncio.sleep(0.1)
    retry_count = 0
    error = None
    while retry_count < 3:
        try:
            received_requests = MockReceivedRequests()
            received_requests["/auth.test"] == expected_count
            break
        except Exception as e:
            error = e
            retry_count += 1
            # waiting for mock_received_requests updates
            await asyncio.sleep(0.1)

    if error is not None:
        raise error
