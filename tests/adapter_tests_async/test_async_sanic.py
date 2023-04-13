import asyncio
import json
from time import time
from urllib.parse import quote

import pytest
from sanic import Sanic
from sanic.request import Request
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.adapter.sanic.async_handler import AsyncSlackRequestHandler
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.oauth.async_oauth_settings import AsyncOAuthSettings
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestSanic:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = AsyncWebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )

    @staticmethod
    def unique_sanic_app_name() -> str:
        return f"awesome-slack-app-{str(time()).replace('.', '-')}"

    @pytest.fixture
    def event_loop(self):
        old_os_env = remove_os_env_temporarily()
        try:
            setup_mock_web_api_server(self)
            loop = asyncio.get_event_loop()
            yield loop
            loop.close()
            cleanup_mock_web_api_server(self)
        finally:
            restore_os_env(old_os_env)

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body,
            timestamp=timestamp,
        )

    def build_headers(self, timestamp: str, body: str):
        content_type = "application/json" if body.startswith("{") else "application/x-www-form-urlencoded"
        return {
            "content-type": content_type,
            "x-slack-signature": self.generate_signature(body, timestamp),
            "x-slack-request-timestamp": timestamp,
        }

    @pytest.mark.asyncio
    async def test_events(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        async def event_handler():
            pass

        app.event("app_mention")(event_handler)

        input = {
            "token": "verification_token",
            "team_id": "T111",
            "enterprise_id": "E111",
            "api_app_id": "A111",
            "event": {
                "client_msg_id": "9cbd4c5b-7ddf-4ede-b479-ad21fca66d63",
                "type": "app_mention",
                "text": "<@W111> Hi there!",
                "user": "W222",
                "ts": "1595926230.009600",
                "team": "T111",
                "channel": "C111",
                "event_ts": "1595926230.009600",
            },
            "type": "event_callback",
            "event_id": "Ev111",
            "event_time": 1595926230,
            "authed_users": ["W111"],
        }
        timestamp, body = str(int(time())), json.dumps(input)

        api = Sanic(name=self.unique_sanic_app_name())
        app_handler = AsyncSlackRequestHandler(app)

        @api.post("/slack/events")
        async def endpoint(req: Request):
            return await app_handler.handle(req)

        _, response = await api.asgi_client.post(
            url="/slack/events",
            content=body,
            headers=self.build_headers(timestamp, body),
        )
        assert response.status_code == 200
        assert_auth_test_count(self, 1)

    @pytest.mark.asyncio
    async def test_shortcuts(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        async def shortcut_handler(ack):
            await ack()

        app.shortcut("test-shortcut")(shortcut_handler)

        input = {
            "type": "shortcut",
            "token": "verification_token",
            "action_ts": "111.111",
            "team": {
                "id": "T111",
                "domain": "workspace-domain",
                "enterprise_id": "E111",
                "enterprise_name": "Org Name",
            },
            "user": {"id": "W111", "username": "primary-owner", "team_id": "T111"},
            "callback_id": "test-shortcut",
            "trigger_id": "111.111.xxxxxx",
        }

        timestamp, body = str(int(time())), f"payload={quote(json.dumps(input))}"

        api = Sanic(name=self.unique_sanic_app_name())
        app_handler = AsyncSlackRequestHandler(app)

        @api.post("/slack/events")
        async def endpoint(req: Request):
            return await app_handler.handle(req)

        _, response = await api.asgi_client.post(
            url="/slack/events",
            content=body,
            headers=self.build_headers(timestamp, body),
        )
        assert response.status_code == 200
        assert_auth_test_count(self, 1)

    @pytest.mark.asyncio
    async def test_commands(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        async def command_handler(ack):
            await ack()

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

        api = Sanic(name=self.unique_sanic_app_name())
        app_handler = AsyncSlackRequestHandler(app)

        @api.post("/slack/events")
        async def endpoint(req: Request):
            return await app_handler.handle(req)

        _, response = await api.asgi_client.post(
            url="/slack/events",
            content=body,
            headers=self.build_headers(timestamp, body),
        )
        assert response.status_code == 200
        assert_auth_test_count(self, 1)

    @pytest.mark.asyncio
    async def test_oauth(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
            oauth_settings=AsyncOAuthSettings(
                client_id="111.111",
                client_secret="xxx",
                scopes=["chat:write", "commands"],
            ),
        )
        api = Sanic(name=self.unique_sanic_app_name())
        app_handler = AsyncSlackRequestHandler(app)

        @api.get("/slack/install")
        async def endpoint(req: Request):
            return await app_handler.handle(req)

        _, response = await api.asgi_client.get(url="/slack/install")
        assert response.status_code == 200
        assert response.headers.get("content-type") == "text/html; charset=utf-8"

        # NOTE: Although sanic-testing 0.6 does not have this value,
        # Sanic apps properly generate the content-length header
        # assert response.headers.get("content-length") == "609"

        assert "https://slack.com/oauth/v2/authorize?state=" in response.text
