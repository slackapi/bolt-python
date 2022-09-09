import json
import time

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt.app import App
from slack_bolt.request import BoltRequest
from slack_bolt.context import BoltContext
from slack_bolt.slack_function import SlackFunction

from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestFunctionBlockActions:
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
            "content-type": ["application/json"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def build_request_from_body(self, message_body: dict) -> BoltRequest:
        timestamp, body = str(int(time.time())), json.dumps(message_body)
        return BoltRequest(body=body, headers=self.build_headers(timestamp, body))

    def test_success(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        func: SlackFunction = app.function("c")(func_listener)
        func.action("a")(simple_listener)

        request = self.build_request_from_body(function_action_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert self.mock_received_requests["/functions.completeSuccess"] == 1

    def test_process_before_response(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
            process_before_response=True,
        )
        func: SlackFunction = app.function("c")(func_listener)
        func.action("a")(simple_listener)

        request = self.build_request_from_body(function_action_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert self.mock_received_requests["/functions.completeSuccess"] == 1

    def test_default_type(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)
        func: SlackFunction = app.function("c")(func_listener)
        func.action({"action_id": "a", "block_id": "b"})(simple_listener)

        request = self.build_request_from_body(function_action_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert self.mock_received_requests["/functions.completeSuccess"] == 1

    def test_default_type_no_block_id(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)
        func: SlackFunction = app.function("c")(func_listener)
        func.action({"action_id": "a"})(simple_listener)

        request = self.build_request_from_body(function_action_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert self.mock_received_requests["/functions.completeSuccess"] == 1

    def test_default_type_and_unmatched_block_id(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)
        func: SlackFunction = app.function("c")(func_listener)
        func.action({"action_id": "a", "block_id": "bbb"})(simple_listener)

        request = self.build_request_from_body(function_action_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert_auth_test_count(self, 1)
        assert "/functions.completeSuccess" not in self.mock_received_requests

    def test_failure(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        request = self.build_request_from_body(function_action_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert_auth_test_count(self, 1)

        app.action("aaa")(simple_listener)
        response = app.dispatch(request)
        assert response.status == 404
        assert_auth_test_count(self, 1)

    def test_failure_2(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        request = self.build_request_from_body(function_action_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert_auth_test_count(self, 1)

        app.block_action("aaa")(simple_listener)
        response = app.dispatch(request)
        assert response.status == 404
        assert_auth_test_count(self, 1)

    def test_success_decorators(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        @app.function("c")
        def func_listener_wrap(body):
            return func_listener(body)

        @func_listener_wrap.action("a")
        def simple_listener_wrap(ack, complete, body, payload, action, client: WebClient, context: BoltContext):
            simple_listener(ack, complete, body, payload, action, client, context)

        request = self.build_request_from_body(function_action_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert self.mock_received_requests["/functions.completeSuccess"] == 1

    def test_success_deconstructed_decorators(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        func: SlackFunction = app.function("c")

        @func
        def func_listener_wrap(body):
            return func_listener(body)

        @func.action("a")
        def simple_listener_wrap(ack, complete, body, payload, action, client: WebClient, context: BoltContext):
            simple_listener(ack, complete, body, payload, action, client, context)

        request = self.build_request_from_body(function_action_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert self.mock_received_requests["/functions.completeSuccess"] == 1

    def test_success_mixed_decorators(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        func: SlackFunction = app.function("c")

        @func
        def func_listener_wrap(body):
            return func_listener(body)

        @func_listener_wrap.action("a")
        def simple_listener_wrap(ack, complete, body, payload, action, client: WebClient, context: BoltContext):
            simple_listener(ack, complete, body, payload, action, client, context)

        request = self.build_request_from_body(function_action_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert self.mock_received_requests["/functions.completeSuccess"] == 1


function_action_body = {
    "type": "block_actions",
    "user": {"id": "U111", "username": "primary-owner", "name": "primary-owner", "team_id": "T111"},
    "api_app_id": "A111",
    "token": "verification_token",
    "container": {"type": "message", "message_ts": "111.222", "channel_id": "C111", "is_ephemeral": False},
    "trigger_id": "111.222.valid",
    "team": {"id": "T111", "domain": "bill-at-tools"},
    "enterprise": None,
    "is_enterprise_install": False,
    "channel": {"id": "C111", "name": "directmessage"},
    "state": {"values": {}},
    "response_url": "https://hooks.slack.com/actions/T111/111/random-value",
    "actions": [
        {
            "action_id": "a",
            "block_id": "b",
            "text": {"type": "plain_text", "text": "Button", "emoji": True},
            "value": "click_me_123",
            "type": "button",
            "style": "primary",
            "action_ts": "111.222.3",
        }
    ],
    "function_data": {
        "execution_id": "Fx111",
        "inputs": {},
        "function": {
            "id": "Fn111",
            "callback_id": "c",
            "title": "A Title",
            "description": "do the thing",
            "type": "app",
            "input_parameters": [],
            "output_parameters": [],
            "app_id": "A111",
            "date_created": 1661459156,
            "date_updated": 1661530445,
            "date_deleted": 0,
        },
    },
    "interactivity": {"interactor": {"secret": "S111", "id": "U111"}, "interactivity_pointer": "111.222.valid"},
    "bot_access_token": "xwfp-valid",
}


def func_listener(body):
    assert body == function_action_body


def simple_listener(ack, complete, body, payload, action, client: WebClient, context: BoltContext):
    assert body["trigger_id"] == "111.222.valid"
    assert body["actions"][0] == payload
    assert payload == action
    assert action["action_id"] == "a"
    assert context.bot_id == "BZYBOTHED"
    assert context.bot_user_id == "W23456789"
    assert context.bot_token == "xoxb-valid"
    assert context.token == "xoxb-valid"
    assert context.user_id == "U111"
    assert context.user_token is None
    assert context.slack_function_bot_access_token == "xwfp-valid"
    assert context.client.token == "xwfp-valid"
    assert client.token == "xwfp-valid"
    ack()
    complete()
