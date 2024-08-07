import json
from time import time
from urllib.parse import quote

import pytest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest
from tests.mock_web_api_server import (
    cleanup_mock_web_api_server_async,
    assert_auth_test_count_async,
    setup_mock_web_api_server_async,
)
from tests.utils import remove_os_env_temporarily, restore_os_env, get_event_loop


body = {
    "type": "view_submission",
    "team": {
        "id": "T111",
        "domain": "workspace-domain",
        "enterprise_id": "E111",
        "enterprise_name": "Sandbox Org",
    },
    "user": {
        "id": "W111",
        "username": "primary-owner",
        "name": "primary-owner",
        "team_id": "T111",
    },
    "api_app_id": "A111",
    "token": "verification_token",
    "trigger_id": "111.222.valid",
    "view": {
        "id": "V111",
        "team_id": "T111",
        "type": "modal",
        "blocks": [
            {
                "type": "input",
                "block_id": "hspI",
                "label": {
                    "type": "plain_text",
                    "text": "Label",
                },
                "optional": False,
                "element": {"type": "plain_text_input", "action_id": "maBWU"},
            }
        ],
        "private_metadata": "This is for you!",
        "callback_id": "view-id",
        "state": {"values": {"hspI": {"maBWU": {"type": "plain_text_input", "value": "test"}}}},
        "hash": "1596530361.3wRYuk3R",
        "title": {
            "type": "plain_text",
            "text": "My App",
        },
        "clear_on_close": False,
        "notify_on_close": False,
        "close": {
            "type": "plain_text",
            "text": "Cancel",
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
        },
        "previous_view_id": None,
        "root_view_id": "V111",
        "app_id": "A111",
        "external_id": "",
        "app_installed_team_id": "T111",
        "bot_id": "B111",
    },
    "response_urls": [],
}

raw_body = f"payload={quote(json.dumps(body))}"


def simple_listener(ack, body, payload, view):
    assert body["trigger_id"] == "111.222.valid"
    assert body["view"] == payload
    assert payload == view
    assert view["private_metadata"] == "This is for you!"
    ack()


response_url_payload_body = {
    "type": "view_submission",
    "team": {"id": "T111", "domain": "test-test-test"},
    "user": {
        "id": "U111",
        "username": "test-test-test",
        "name": "test-test-test",
        "team_id": "T111",
    },
    "api_app_id": "A111",
    "token": "verification-token",
    "trigger_id": "111.222.xxx",
    "view": {
        "id": "V111",
        "team_id": "T111",
        "type": "modal",
        "blocks": [],
        "callback_id": "view-id",
        "state": {},
        "title": {
            "type": "plain_text",
            "text": "My App",
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
        },
        "previous_view_id": None,
        "root_view_id": "V111",
        "app_id": "A111",
        "external_id": "",
        "app_installed_team_id": "T111",
        "bot_id": "B111",
    },
    "response_urls": [
        {
            "block_id": "b",
            "action_id": "a",
            "channel_id": "C111",
            "response_url": "http://localhost:8888/webhook",
        }
    ],
    "is_enterprise_install": False,
}


raw_response_url_body = f"payload={quote(json.dumps(response_url_payload_body))}"


connect_channel_payload = {
    "type": "view_submission",
    "team": {
        "id": "T-other-side",
        "domain": "other-side",
        "enterprise_id": "E-other-side",
        "enterprise_name": "Kaz Sandbox Org",
    },
    "user": {"id": "W111", "username": "kaz", "name": "kaz", "team_id": "T-other-side"},
    "api_app_id": "A1111",
    "token": "legacy-fixed-token",
    "trigger_id": "111.222.xxx",
    "view": {
        "id": "V11111",
        "team_id": "T-other-side",
        "type": "modal",
        "blocks": [
            {
                "type": "input",
                "block_id": "zniAM",
                "label": {"type": "plain_text", "text": "Label"},
                "element": {
                    "type": "plain_text_input",
                    "dispatch_action_config": {"trigger_actions_on": ["on_enter_pressed"]},
                    "action_id": "qEJr",
                },
            }
        ],
        "private_metadata": "",
        "callback_id": "view-id",
        "state": {"values": {"zniAM": {"qEJr": {"type": "plain_text_input", "value": "Hi there!"}}}},
        "hash": "1664950703.CmTS8F7U",
        "title": {"type": "plain_text", "text": "My App"},
        "close": {"type": "plain_text", "text": "Cancel"},
        "submit": {"type": "plain_text", "text": "Submit"},
        "root_view_id": "V00000",
        "app_id": "A1111",
        "external_id": "",
        "app_installed_team_id": "T-installed-workspace",
        "bot_id": "B1111",
    },
    "enterprise": {"id": "E-other-side", "name": "Kaz Sandbox Org"},
}

connect_channel_body = f"payload={quote(json.dumps(connect_channel_payload))}"


class TestAsyncViewSubmission:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
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
            setup_mock_web_api_server_async(self)
            loop = get_event_loop()
            yield loop
            loop.close()
            cleanup_mock_web_api_server_async(self)
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

    def build_valid_request(self, body: str = raw_body) -> AsyncBoltRequest:
        timestamp = str(int(time()))
        return AsyncBoltRequest(body=body, headers=self.build_headers(timestamp, body))

    @pytest.mark.asyncio
    async def test_mock_server_is_running(self):
        resp = await self.web_client.api_test()
        assert resp != None

    @pytest.mark.asyncio
    async def test_success(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.view("view-id")(simple_listener)

        request = self.build_valid_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_success_2(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.view_submission("view-id")(simple_listener)

        request = self.build_valid_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_process_before_response(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
            process_before_response=True,
        )
        app.view("view-id")(simple_listener)

        request = self.build_valid_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_failure(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        request = self.build_valid_request()
        response = await app.async_dispatch(request)
        assert response.status == 404
        await assert_auth_test_count_async(self, 1)

        app.view("view-idddd")(simple_listener)
        response = await app.async_dispatch(request)
        assert response.status == 404
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_failure_2(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        request = self.build_valid_request()
        response = await app.async_dispatch(request)
        assert response.status == 404
        await assert_auth_test_count_async(self, 1)

        app.view_submission("view-idddd")(simple_listener)
        response = await app.async_dispatch(request)
        assert response.status == 404
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_response_urls(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        @app.view("view-id")
        async def check(ack, respond):
            await respond("Hi")
            await ack()

        request = self.build_valid_request(raw_response_url_body)
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_connected_channels(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.view("view-id")(verify_connected_channel)

        request = self.build_valid_request(body=connect_channel_body)
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)


async def simple_listener(ack, body, payload, view):
    assert body["trigger_id"] == "111.222.valid"
    assert body["view"] == payload
    assert payload == view
    assert view["private_metadata"] == "This is for you!"
    await ack()


async def verify_connected_channel(ack, context):
    assert context.team_id == "T-installed-workspace"
    await ack()
