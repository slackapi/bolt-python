import json
import time
import pytest

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.signature import SignatureVerifier

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.slack_function import SlackFunction

from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count_async,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestFunctionViewSubmission:
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
        return {
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def build_request_from_body(self, message_body: dict) -> AsyncBoltRequest:
        timestamp, body = str(int(time.time())), json.dumps(message_body)
        return AsyncBoltRequest(body=body, headers=self.build_headers(timestamp, body))

    @pytest.mark.asyncio
    async def test_mock_server_is_running(self):
        resp = await self.web_client.api_test()
        assert resp != None

    @pytest.mark.asyncio
    async def test_success_view(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        func: SlackFunction = app.function("c")
        func.view("view-id")(simple_listener)

        request = self.build_request_from_body(function_view_submission_body)
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)
        assert self.mock_received_requests["/functions.completeSuccess"] == 1

    @pytest.mark.asyncio
    async def test_success_view_submission(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        func: SlackFunction = app.function("c")
        func.view_submission("view-id")(simple_listener)

        request = self.build_request_from_body(function_view_submission_body)
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)
        assert self.mock_received_requests["/functions.completeSuccess"] == 1

    @pytest.mark.asyncio
    async def test_failure_view(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        request = self.build_request_from_body(function_view_submission_body)
        response = await app.async_dispatch(request)
        assert response.status == 404
        await assert_auth_test_count_async(self, 1)

        func: SlackFunction = app.function("c")
        func.view("view-idddd")(simple_listener)
        response = await app.async_dispatch(request)
        assert response.status == 404
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_failure_view_submission(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        request = self.build_request_from_body(function_view_submission_body)
        response = await app.async_dispatch(request)
        assert response.status == 404
        await assert_auth_test_count_async(self, 1)

        func: SlackFunction = app.function("c")
        func.view_submission("view-idddd")(simple_listener)
        response = await app.async_dispatch(request)
        assert response.status == 404
        await assert_auth_test_count_async(self, 1)


function_view_submission_body = {
    "type": "view_submission",
    "team": {"id": "T111", "domain": "workspace-domain"},
    "enterprise": None,
    "user": {"id": "U111", "name": "primary-owner", "team_id": "T111"},
    "view": {
        "id": "V111",
        "team_id": "T111",
        "app_id": "A111",
        "app_installed_team_id": "T111",
        "bot_id": "B111",
        "title": {"type": "plain_text", "text": "Sample modal title", "emoji": True},
        "type": "modal",
        "blocks": [
            {
                "type": "input",
                "block_id": "input_block_id",
                "label": {"type": "plain_text", "text": "What are your hopes and dreams?", "emoji": True},
                "optional": False,
                "dispatch_action": False,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sample_input_id",
                    "multiline": True,
                    "dispatch_action_config": {"trigger_actions_on": ["on_enter_pressed"]},
                },
            }
        ],
        "close": None,
        "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
        "state": {"values": {"input_block_id": {"sample_input_id": {"type": "plain_text_input", "value": "hello world"}}}},
        "hash": "123.abc",
        "private_metadata": "This is for you!",
        "callback_id": "view-id",
        "root_view_id": "V111",
        "previous_view_id": None,
        "clear_on_close": False,
        "notify_on_close": True,
        "external_id": "",
    },
    "api_app_id": "A111",
    "response_urls": [],
    "bot_access_token": "xwfp-111",
    "function_data": {
        "execution_id": "Fx111",
        "function": {"callback_id": "c"},
        "inputs": {
            "interactivity": {
                "interactor": {
                    "id": "U111",
                    "secret": "NDA111",
                },
                "interactivity_pointer": "123.123.acb1",
            },
            "interactivity.interactor": {
                "id": "U111",
                "secret": "NDA111",
            },
            "interactivity.interactor.id": "U111",
            "interactivity.interactor.secret": "NDA111",
            "interactivity.interactivity_pointer": "123.123.acb1",
        },
    },
    "interactivity": {
        "interactor": {
            "secret": "NDA111",
            "id": "U111",
        },
        "interactivity_pointer": "123.123.acb1",
    },
}


async def simple_listener(ack, body, payload, view, complete):
    await ack()
    assert body["interactivity"]["interactivity_pointer"] == "123.123.acb1"
    assert body["view"] == payload
    assert payload == view
    assert view["private_metadata"] == "This is for you!"
    await complete()
