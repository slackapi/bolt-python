import asyncio
import json
from time import time
from urllib.parse import quote

import pytest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt import BoltResponse
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.authorization import AuthorizeResult
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.request.payload_utils import is_event
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count_async,
)
from tests.utils import remove_os_env_temporarily, restore_os_env

valid_token = "xoxb-valid"
valid_user_token = "xoxp-valid"


async def authorize(enterprise_id, team_id, user_id, client: AsyncWebClient):
    assert enterprise_id == "E111"
    assert team_id == "T111"
    assert user_id == "W99999"
    auth_test = await client.auth_test(token=valid_token)
    return AuthorizeResult.from_auth_test_response(
        auth_test_response=auth_test,
        bot_token=valid_token,
    )


async def user_authorize(enterprise_id, team_id, user_id, client: AsyncWebClient):
    assert enterprise_id == "E111"
    assert team_id == "T111"
    assert user_id == "W99999"
    auth_test = await client.auth_test(token=valid_user_token)
    return AuthorizeResult.from_auth_test_response(
        auth_test_response=auth_test,
        user_token=valid_user_token,
    )


async def error_authorize(enterprise_id, team_id, user_id):
    assert enterprise_id == "E111"
    assert team_id == "T111"
    assert user_id == "W99999"
    return None


class TestAsyncAuthorize:
    signing_secret = "secret"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = AsyncWebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )

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
        return {
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def build_block_actions_request(self) -> AsyncBoltRequest:
        timestamp = str(int(time()))
        return AsyncBoltRequest(body=block_actions_raw_body, headers=self.build_headers(timestamp, block_actions_raw_body))

    def build_message_changed_event_request(self) -> AsyncBoltRequest:
        timestamp = str(int(time()))
        raw_body = json.dumps(
            {
                "token": "verification_token",
                "team_id": "T111",
                "enterprise_id": "E111",
                "api_app_id": "A111",
                "event": {
                    "type": "message",
                    "subtype": "message_changed",
                    "channel": "C2147483705",
                    "ts": "1358878755.000001",
                    "message": {
                        "type": "message",
                        "user": "U2147483697",
                        "text": "Hello, world!",
                        "ts": "1355517523.000005",
                        "edited": {"user": "U2147483697", "ts": "1358878755.000001"},
                    },
                },
                "type": "event_callback",
                "event_id": "Ev111",
                "event_time": 1599616881,
                "authed_users": ["W111"],
            }
        )
        return AsyncBoltRequest(body=raw_body, headers=self.build_headers(timestamp, raw_body))

    @pytest.mark.asyncio
    async def test_success(self):
        app = AsyncApp(
            client=self.web_client,
            authorize=authorize,
            signing_secret=self.signing_secret,
        )
        app.action("a")(simple_listener)

        request = self.build_block_actions_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert response.body == ""
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_failure(self):
        app = AsyncApp(
            client=self.web_client,
            authorize=error_authorize,
            signing_secret=self.signing_secret,
        )
        app.block_action("a")(simple_listener)

        request = self.build_block_actions_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert response.body == ""
        assert self.mock_received_requests.get("/auth.test") == None

    @pytest.mark.asyncio
    async def test_bot_context_attributes(self):
        app = AsyncApp(
            client=self.web_client,
            authorize=authorize,
            signing_secret=self.signing_secret,
        )
        app.action("a")(assert_bot_context_attributes)

        request = self.build_block_actions_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert response.body == ""
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_user_context_attributes(self):
        app = AsyncApp(
            client=self.web_client,
            authorize=user_authorize,
            signing_secret=self.signing_secret,
        )
        app.action("a")(assert_user_context_attributes)

        request = self.build_block_actions_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert response.body == ""
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_user_context_attributes(self):
        async def skip_message_changed_events(body: dict, payload: dict, next_):
            if is_event(body) and payload.get("type") == "message" and payload.get("subtype") == "message_changed":
                return BoltResponse(status=200, body="as expected")
            await next_()

        app = AsyncApp(
            client=self.web_client,
            before_authorize=skip_message_changed_events,
            authorize=user_authorize,
            signing_secret=self.signing_secret,
        )
        app.action("a")(assert_user_context_attributes)

        request = self.build_block_actions_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert response.body == ""
        await assert_auth_test_count_async(self, 1)

        request = self.build_message_changed_event_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert response.body == "as expected"
        await assert_auth_test_count_async(self, 1)  # should be skipped


block_actions_body = {
    "type": "block_actions",
    "user": {
        "id": "W99999",
        "username": "primary-owner",
        "name": "primary-owner",
        "team_id": "T111",
    },
    "api_app_id": "A111",
    "token": "verification_token",
    "container": {
        "type": "message",
        "message_ts": "111.222",
        "channel_id": "C111",
        "is_ephemeral": True,
    },
    "trigger_id": "111.222.valid",
    "team": {
        "id": "T111",
        "domain": "workspace-domain",
        "enterprise_id": "E111",
        "enterprise_name": "Sandbox Org",
    },
    "channel": {"id": "C111", "name": "test-channel"},
    "response_url": "https://hooks.slack.com/actions/T111/111/random-value",
    "actions": [
        {
            "action_id": "a",
            "block_id": "b",
            "text": {"type": "plain_text", "text": "Button", "emoji": True},
            "value": "click_me_123",
            "type": "button",
            "action_ts": "1596530385.194939",
        }
    ],
}

block_actions_raw_body = f"payload={quote(json.dumps(block_actions_body))}"


async def simple_listener(ack, body, payload, action):
    assert body["trigger_id"] == "111.222.valid"
    assert body["actions"][0] == payload
    assert payload == action
    assert action["action_id"] == "a"
    await ack()


async def assert_bot_context_attributes(ack, context):
    assert context["bot_id"] == "BZYBOTHED"
    assert context["bot_user_id"] == "W23456789"
    assert context["bot_token"] == "xoxb-valid"
    assert context["token"] == "xoxb-valid"
    assert context["user_id"] == "W99999"
    assert context.get("user_token") is None
    await ack()


async def assert_user_context_attributes(ack, context):
    assert context.get("bot_id") is None
    assert context.get("bot_user_id") is None
    assert context.get("bot_token") is None
    assert context["token"] == "xoxp-valid"
    assert context["user_id"] == "W99999"
    assert context["user_token"] == "xoxp-valid"
    await ack()
