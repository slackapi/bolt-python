import json
import time

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt.app import App
from slack_bolt.slack_function import SlackFunction
from slack_bolt.request import BoltRequest
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestFunctionViewClosed:
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

    def build_headers(self, timestamp: str, body: str):
        return {
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def build_request_from_body(self, message_body: dict) -> BoltRequest:
        timestamp, body = str(int(time.time())), json.dumps(message_body)
        return BoltRequest(body=body, headers=self.build_headers(timestamp, body))

    def test_mock_server_is_running(self):
        resp = self.web_client.api_test()
        assert resp != None

    def test_success(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        func: SlackFunction = app.function("c")
        func.view({"type": "view_closed", "callback_id": "view-id"})(simple_listener)

        request = self.build_request_from_body(function_view_closed_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert self.mock_received_requests["/functions.completeSuccess"] == 1

    def test_success_view_closed(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        func: SlackFunction = app.function("c")
        func.view_closed("view-id")(simple_listener)

        request = self.build_request_from_body(function_view_closed_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert self.mock_received_requests["/functions.completeSuccess"] == 1

    def test_failure_view(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        func: SlackFunction = app.function("c")

        request = self.build_request_from_body(function_view_closed_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert_auth_test_count(self, 1)

        func.view({"type": "view_closed", "callback_id": "view-idddd"})(simple_listener)
        response = app.dispatch(request)
        assert response.status == 404
        assert_auth_test_count(self, 1)

    def test_failure_view_closed(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        request = self.build_request_from_body(function_view_closed_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert_auth_test_count(self, 1)

        func: SlackFunction = app.function("c")
        func.view_closed("view-idddd")(simple_listener)
        response = app.dispatch(request)
        assert response.status == 404
        assert_auth_test_count(self, 1)


function_view_closed_body = {
    "type": "view_closed",
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
        "state": {"values": {}},
        "hash": "123.aBc1",
        "private_metadata": "This is for you!",
        "callback_id": "view-id",
        "root_view_id": "V111",
        "previous_view_id": None,
        "clear_on_close": False,
        "notify_on_close": True,
        "external_id": "",
    },
    "api_app_id": "A111",
    "is_cleared": False,
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
                "interactivity_pointer": "123.123.abc1",
            },
            "interactivity.interactor": {
                "id": "U111",
                "secret": "NDA111",
            },
            "interactivity.interactor.id": "U111",
            "interactivity.interactor.secret": "NDA111",
            "interactivity.interactivity_pointer": "123.123.abc1",
        },
    },
}


def simple_listener(ack, body, payload, view, complete):
    ack()
    assert body["view"] == payload
    assert payload == view
    assert view["private_metadata"] == "This is for you!"
    complete()
