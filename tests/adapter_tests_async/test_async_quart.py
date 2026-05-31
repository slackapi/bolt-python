import json
import sys
from time import time
from urllib.parse import quote

import pytest
from slack_sdk.oauth.state_store.async_state_store import AsyncOAuthStateStore
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.oauth.async_oauth_settings import AsyncOAuthSettings
from tests.mock_web_api_server import (
    assert_auth_test_count,
    cleanup_mock_web_api_server,
    setup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env

pytestmark = pytest.mark.skipif(sys.version_info < (3, 9), reason="Quart requires Python 3.9+")

if sys.version_info >= (3, 9):
    from slack_bolt.adapter.quart.async_handler import AsyncSlackRequestHandler
    from quart import Quart, request


class TestAsyncStateStore(AsyncOAuthStateStore):
    async def async_issue(self, *args, **kwargs) -> str:
        return "uuid4-value"

    async def async_consume(self, state: str) -> bool:
        return state == "uuid4-value"


class TestAsyncQuart:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = AsyncWebClient(
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

    def build_headers(self, timestamp: str, body: str):
        content_type = "application/json" if body.startswith("{") else "application/x-www-form-urlencoded"
        return {
            "content-type": content_type,
            "x-slack-signature": self.generate_signature(body, timestamp),
            "x-slack-request-timestamp": timestamp,
        }

    def build_app(self, oauth_settings=None):
        return AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
            oauth_settings=oauth_settings,
        )

    def build_client(self, app, path: str = "/slack/events", method: str = "POST", addition_context_properties=None):
        api = Quart(__name__)
        app_handler = AsyncSlackRequestHandler(app)

        async def endpoint():
            return await app_handler.handle(request, addition_context_properties)

        api.add_url_rule(path, "endpoint", endpoint, methods=[method])
        return api.test_client()

    def build_event_body(self) -> str:
        return json.dumps(
            {
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
        )

    @pytest.mark.asyncio
    async def test_events(self):
        app = self.build_app()

        async def event_handler():
            pass

        app.event("app_mention")(event_handler)

        timestamp, body = str(int(time())), self.build_event_body()
        client = self.build_client(app)
        response = await client.post(
            "/slack/events",
            data=body,
            headers=self.build_headers(timestamp, body),
        )
        assert response.status_code == 200
        assert_auth_test_count(self, 1)

    @pytest.mark.asyncio
    async def test_events_with_additional_context_properties(self):
        app = self.build_app()
        observed_context = {}

        async def event_handler(context):
            observed_context["custom_value"] = context["custom_value"]

        app.event("app_mention")(event_handler)

        timestamp, body = str(int(time())), self.build_event_body()
        client = self.build_client(app, addition_context_properties={"custom_value": "quart"})
        response = await client.post(
            "/slack/events",
            data=body,
            headers=self.build_headers(timestamp, body),
        )
        assert response.status_code == 200
        assert observed_context["custom_value"] == "quart"
        assert_auth_test_count(self, 1)

    @pytest.mark.asyncio
    async def test_shortcuts(self):
        app = self.build_app()

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

        client = self.build_client(app)
        response = await client.post(
            "/slack/events",
            data=body,
            headers=self.build_headers(timestamp, body),
        )
        assert response.status_code == 200
        assert_auth_test_count(self, 1)

    @pytest.mark.asyncio
    async def test_commands(self):
        app = self.build_app()

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

        client = self.build_client(app)
        response = await client.post(
            "/slack/events",
            data=body,
            headers=self.build_headers(timestamp, body),
        )
        assert response.status_code == 200
        assert_auth_test_count(self, 1)

    @pytest.mark.asyncio
    async def test_oauth(self):
        app = self.build_app(
            oauth_settings=AsyncOAuthSettings(
                client_id="111.111",
                client_secret="xxx",
                scopes=["chat:write", "commands"],
            ),
        )

        client = self.build_client(app, path="/slack/install", method="GET")
        response = await client.get("/slack/install")
        assert response.status_code == 200
        assert response.headers.get("content-type") == "text/html; charset=utf-8"
        assert response.headers.get("set-cookie") is not None
        assert "https://slack.com/oauth/v2/authorize?state=" in await response.get_data(as_text=True)

    @pytest.mark.asyncio
    async def test_oauth_callback(self):
        app = self.build_app(
            oauth_settings=AsyncOAuthSettings(
                client_id="111.111",
                client_secret="xxx",
                scopes=["chat:write", "commands"],
                state_store=TestAsyncStateStore(),
            ),
        )

        client = self.build_client(app, path="/slack/oauth_redirect", method="GET")
        response = await client.get(
            "/slack/oauth_redirect?code=1234567890&state=uuid4-value",
            headers={"Cookie": "slack-app-oauth-state=uuid4-value"},
        )
        assert response.status_code == 200
        assert response.headers.get("content-type") == "text/html; charset=utf-8"
        assert await response.get_data(as_text=True) is not None

    @pytest.mark.asyncio
    async def test_url_verification(self):
        app = self.build_app()

        input = {
            "token": "Jhj5dZrVaK7ZwHHjRyZWjbDl",
            "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P",
            "type": "url_verification",
        }

        timestamp, body = str(int(time())), json.dumps(input)

        client = self.build_client(app)
        response = await client.post(
            "/slack/events",
            data=body,
            headers=self.build_headers(timestamp, body),
        )
        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json;charset=utf-8"
        assert json.loads(await response.get_data(as_text=True)) == {"challenge": input["challenge"]}
        assert_auth_test_count(self, 0)

    @pytest.mark.asyncio
    async def test_not_found(self):
        app = self.build_app()
        client = self.build_client(app, path="/slack/unknown", method="GET")
        response = await client.get("/slack/unknown")
        assert response.status_code == 404
        assert "Not Found" == await response.get_data(as_text=True)
