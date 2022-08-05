import json
import time

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt.app import App
from slack_bolt.request import BoltRequest
from tests.mock_web_api_server import (
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
        assert self.mock_received_requests["/functions.completeSuccess"] == 1

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
        assert self.mock_received_requests["/functions.completeError"] == 1

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
    },
    "type": "event_callback",
    "event_id": "Ev111",
    "event_time": 1659055013,
    "authed_users": ["W111"],
}


def reverse(body, event, complete_success):
    assert body == function_body
    assert event == function_body["event"]
    complete_success(
        {
            "reverseString": "olleh",
        }
    )


def reverse_error(body, event, complete_error):
    assert body == function_body
    assert event == function_body["event"]
    complete_error("there was an error")
