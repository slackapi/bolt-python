import json
import logging
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler
from typing import Optional
from urllib.parse import ParseResult, parse_qs, urlparse


class MockHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    default_request_version = "HTTP/1.1"
    logger = logging.getLogger(__name__)

    def is_valid_token(self):
        return "Authorization" in self.headers and str(self.headers["Authorization"]).startswith("Bearer xoxb-")

    def is_valid_user_token(self):
        return "Authorization" in self.headers and str(self.headers["Authorization"]).startswith("Bearer xoxp-")

    def set_common_headers(self, content_length: int = 0):
        self.send_header("content-type", "application/json;charset=utf-8")
        self.send_header("content-length", str(content_length))
        self.end_headers()

    def _handle(self):
        parsed_path: ParseResult = urlparse(self.path)
        path = parsed_path.path
        # put_nowait is common between Queue & asyncio.Queue, it does not need to be awaited
        self.server.queue.put_nowait(path)
        try:
            if path == "/webhook":
                self.send_response(200)
                self.set_common_headers(len("OK"))
                self.wfile.write("OK".encode("utf-8"))
                return

            body = """{"ok": true}"""
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
                                self.set_common_headers(len(OAUTH_V2_ACCESS_BOT_REFRESH_RESPONSE))
                                self.wfile.write(OAUTH_V2_ACCESS_BOT_REFRESH_RESPONSE.encode("utf-8"))
                                return
                            if "user-valid" in refresh_token:
                                self.send_response(200)
                                self.set_common_headers(len(OAUTH_V2_ACCESS_USER_REFRESH_RESPONSE))
                                self.wfile.write(OAUTH_V2_ACCESS_USER_REFRESH_RESPONSE.encode("utf-8"))
                                return
                    elif request_body.get("code") is not None:
                        self.send_response(200)
                        self.set_common_headers(len(OAUTH_V2_ACCESS_RESPONSE))
                        self.wfile.write(OAUTH_V2_ACCESS_RESPONSE.encode("utf-8"))
                        return

            if self.is_valid_user_token():
                if path == "/auth.test":
                    self.send_response(200)
                    self.send_header("x-oauth-scopes", "chat:write,search:read")
                    self.set_common_headers(len(USER_AUTH_TEST_RESPONSE))
                    self.wfile.write(USER_AUTH_TEST_RESPONSE.encode("utf-8"))
                    return

            if self.is_valid_token():
                if path == "/auth.test":
                    self.send_response(200)
                    self.send_header("x-oauth-scopes", "chat:write,commands")
                    self.set_common_headers(len(BOT_AUTH_TEST_RESPONSE))
                    self.wfile.write(BOT_AUTH_TEST_RESPONSE.encode("utf-8"))
                    return

                request_body = self._parse_request_body(
                    parsed_path=parsed_path,
                    content_len=int(self.headers.get("Content-Length") or 0),
                )
                self.logger.info(f"request: {path} {request_body}")

                header = self.headers["authorization"]
                pattern = str(header).split("xoxb-", 1)[1]
                if pattern.isnumeric():
                    self.send_response(int(pattern))
                    self.set_common_headers(len(OK_FALSE_RESPONSE))
                    self.wfile.write(OK_FALSE_RESPONSE.encode("utf-8"))
                    return
            else:
                body = INVALID_AUTH

            self.send_response(HTTPStatus.OK)
            self.set_common_headers(len(body))
            self.wfile.write(body.encode("utf-8"))

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


INVALID_AUTH = json.dumps(
    {
        "ok": False,
        "error": "invalid_auth",
    }
)

OK_FALSE_RESPONSE = json.dumps(
    {
        "ok": False,
    }
)

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
