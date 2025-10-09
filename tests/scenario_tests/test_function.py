import json
import re
import time
import pytest
from unittest.mock import Mock

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt.app import App
from slack_bolt.request import BoltRequest
from tests.mock_web_api_server import (
    assert_received_request_count,
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestFunction:
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

    def setup_time_mocks(self, *, monkeypatch: pytest.MonkeyPatch, time_mock: Mock, sleep_mock: Mock):
        monkeypatch.setattr(time, "time", time_mock)
        monkeypatch.setattr(time, "sleep", sleep_mock)

    def test_valid_callback_id_success(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse")(reverse)

        request = self.build_request_from_body(function_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert_received_request_count(self, "/functions.completeSuccess", 1)

    def test_valid_callback_id_complete(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse")(complete_it)

        request = self.build_request_from_body(function_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert_received_request_count(self, "/functions.completeSuccess", 1)

    def test_valid_callback_id_error(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse")(reverse_error)

        request = self.build_request_from_body(function_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert_received_request_count(self, "/functions.completeError", 1)

    def test_invalid_callback_id(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse")(reverse)

        request = self.build_request_from_body(wrong_id_function_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert_auth_test_count(self, 1)

    def test_invalid_declaration(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        func = app.function("reverse")

        with pytest.raises(TypeError):
            func("hello world")

    def test_auto_acknowledge_false_with_acknowledging(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse", auto_acknowledge=False)(just_ack)

        request = self.build_request_from_body(function_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)

    def test_auto_acknowledge_false_without_acknowledging(self, caplog, monkeypatch):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse", auto_acknowledge=False)(just_no_ack)

        request = self.build_request_from_body(function_body)
        self.setup_time_mocks(
            monkeypatch=monkeypatch,
            time_mock=Mock(side_effect=[current_time for current_time in range(100)]),
            sleep_mock=Mock(),
        )
        response = app.dispatch(request)

        assert response.status == 404
        assert_auth_test_count(self, 1)
        assert f"WARNING {just_no_ack.__name__} didn't call ack()" in caplog.text

    def test_function_handler_timeout(self, monkeypatch):
        timeout = 5
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse", auto_acknowledge=False, ack_timeout=timeout)(just_no_ack)
        request = self.build_request_from_body(function_body)

        sleep_mock = Mock()
        self.setup_time_mocks(
            monkeypatch=monkeypatch,
            time_mock=Mock(side_effect=[current_time for current_time in range(100)]),
            sleep_mock=sleep_mock,
        )

        response = app.dispatch(request)

        assert response.status == 404
        assert_auth_test_count(self, 1)
        assert (
            sleep_mock.call_count == timeout
        ), f"Expected handler to time out after calling time.sleep 5 times, but it was called {sleep_mock.call_count} times"

    def test_warning_when_timeout_improperly_set(self, caplog):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse")(just_no_ack)
        assert "WARNING" not in caplog.text

        timeout_argument_name = "ack_timeout"
        kwargs = {timeout_argument_name: 5}

        callback_id = "reverse1"
        app.function(callback_id, **kwargs)(just_no_ack)
        assert (
            f'WARNING On @app.function("{callback_id}"), as `auto_acknowledge` is `True`, `{timeout_argument_name}={kwargs[timeout_argument_name]}` you gave will be unused'
            in caplog.text
        )

        callback_id = re.compile(r"hello \w+")
        app.function(callback_id, **kwargs)(just_no_ack)
        assert (
            f"WARNING On @app.function({callback_id}), as `auto_acknowledge` is `True`, `{timeout_argument_name}={kwargs[timeout_argument_name]}` you gave will be unused"
            in caplog.text
        )


function_body = {
    "token": "verification_token",
    "enterprise_id": "E111",
    "team_id": "T111",
    "api_app_id": "A111",
    "event": {
        "type": "function_executed",
        "function": {
            "id": "Fn111",
            "callback_id": "reverse",
            "title": "Reverse",
            "description": "Takes a string and reverses it",
            "type": "app",
            "input_parameters": [
                {
                    "type": "string",
                    "name": "stringToReverse",
                    "description": "The string to reverse",
                    "title": "String To Reverse",
                    "is_required": True,
                }
            ],
            "output_parameters": [
                {
                    "type": "string",
                    "name": "reverseString",
                    "description": "The string in reverse",
                    "title": "Reverse String",
                    "is_required": True,
                }
            ],
            "app_id": "A111",
            "date_updated": 1659054991,
        },
        "inputs": {"stringToReverse": "hello"},
        "function_execution_id": "Fx111",
        "event_ts": "1659055013.509853",
        "bot_access_token": "xwfp-valid",
    },
    "type": "event_callback",
    "event_id": "Ev111",
    "event_time": 1659055013,
    "authed_users": ["W111"],
}

wrong_id_function_body = {
    "token": "verification_token",
    "enterprise_id": "E111",
    "team_id": "T111",
    "api_app_id": "A111",
    "event": {
        "type": "function_executed",
        "function": {
            "id": "Fn111",
            "callback_id": "wrong_callback_id",
            "title": "Reverse",
            "description": "Takes a string and reverses it",
            "type": "app",
            "input_parameters": [
                {
                    "type": "string",
                    "name": "stringToReverse",
                    "description": "The string to reverse",
                    "title": "String To Reverse",
                    "is_required": True,
                }
            ],
            "output_parameters": [
                {
                    "type": "string",
                    "name": "reverseString",
                    "description": "The string in reverse",
                    "title": "Reverse String",
                    "is_required": True,
                }
            ],
            "app_id": "A111",
            "date_updated": 1659054991,
        },
        "inputs": {"stringToReverse": "hello"},
        "function_execution_id": "Fx111",
        "event_ts": "1659055013.509853",
        "bot_access_token": "xwfp-valid",
    },
    "type": "event_callback",
    "event_id": "Ev111",
    "event_time": 1659055013,
    "authed_users": ["W111"],
}


def reverse(body, event, context, client, complete, inputs):
    assert body == function_body
    assert event == function_body["event"]
    assert inputs == function_body["event"]["inputs"]
    assert context.function_execution_id == "Fx111"
    assert complete.function_execution_id == "Fx111"
    assert context.function_bot_access_token == "xwfp-valid"
    assert context.client.token == "xwfp-valid"
    assert client.token == "xwfp-valid"
    assert complete.client.token == "xwfp-valid"
    assert complete.has_been_called() is False
    complete(
        outputs={"reverseString": "olleh"},
    )
    assert complete.has_been_called() is True


def reverse_error(body, event, fail):
    assert body == function_body
    assert event == function_body["event"]
    assert fail.function_execution_id == "Fx111"
    assert fail.has_been_called() is False
    fail(error="there was an error")
    assert fail.has_been_called() is True


def complete_it(body, event, complete):
    assert body == function_body
    assert event == function_body["event"]
    complete(outputs={})


def just_ack(ack, body, event):
    assert body == function_body
    assert event == function_body["event"]
    ack()


def just_no_ack(body, event):
    assert body == function_body
    assert event == function_body["event"]
