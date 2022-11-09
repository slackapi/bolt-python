import json
from time import time
import pytest

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt.adapter.asgi.handler import SlackRequestHandler
from slack_bolt.app import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsgi:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = WebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body,
            timestamp=timestamp,
        )

    def build_raw_headers(self, timestamp: str, body: str):
        content_type = "application/json" if body.startswith("{") else "application/x-www-form-urlencoded"
        return [
            (b"host", b"123.123.123"),
            (b"user-agent", b"some slack thing"),
            (b"content-length", b"426"),
            (b"accept", b"application/json,*/*"),
            (b"accept-encoding", b"gzip,deflate"),
            (b"content-type", bytes(content_type, "latin-1")),
            (b"x-forwarded-for", b"123.123.123"),
            (b"x-forwarded-proto", b"https"),
            (b"x-slack-request-timestamp", bytes(timestamp, "latin-1")),
            (b"x-slack-signature", bytes(self.generate_signature(body, timestamp), "latin-1")),
        ]

    def build_scope(self, method: str, path: str, timestamp, body):
        return {
            "type": "http",
            "method": method,
            "path": path,
            "raw_path": bytes(path, "latin-1"),
            "query_string": b"",
            "headers": self.build_raw_headers(timestamp, body),
        }

    @pytest.mark.asyncio
    async def test_commands(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        def command_handler(ack):
            ack()

        app.command("/hello-world")(command_handler)

        input = (
            "token=verification_token"
            "&team_id=T111"
            "&team_domain=test-domain"
            "&channel_id=C111"
            "&channel_name=random"
            "&user_id=W111"
            "&user_name=primary-owner"
            "&command=%2Fhello-world"
            "&text=Hi"
            "&enterprise_id=E111"
            "&enterprise_name=Org+Name"
            "&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT111%2F111%2Fxxxxx"
            "&trigger_id=111.111.xxx"
        )
        timestamp, body = str(int(time())), input

        scope = self.build_scope("POST", "/slack/events", timestamp, body)

        async def receive():
            return {"type": "http.request", "body": bytes(body, "latin-1"), "more_body": False}

        asgi_app = SlackRequestHandler(app)

        response = await asgi_app(scope, receive, None)

        assert response.status_code == 200
        assert response.headers.get("content-type") == "text/plain;charset=utf-8"
        assert_auth_test_count(self, 1)
