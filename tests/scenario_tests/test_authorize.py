import json
from time import time
from urllib.parse import quote

from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier

from slack_bolt import BoltRequest
from slack_bolt.app import App
from slack_bolt.authorization import AuthorizationResult
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env

valid_token = "xoxb-valid"


def authorize(enterprise_id, team_id, user_id, client: WebClient):
    assert enterprise_id == "E111"
    assert team_id == "T111"
    assert user_id == "W111"
    auth_test = client.auth_test(token=valid_token)
    return AuthorizationResult.from_auth_test_response(
        auth_test_response=auth_test, bot_token=valid_token,
    )


def error_authorize(enterprise_id, team_id, user_id):
    assert enterprise_id == "E111"
    assert team_id == "T111"
    assert user_id == "W111"
    return None


class TestAuthorize:
    signing_secret = "secret"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = WebClient(token=valid_token, base_url=mock_api_server_base_url,)

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body, timestamp=timestamp,
        )

    def build_headers(self, timestamp: str, body: str):
        return {
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def build_valid_request(self) -> BoltRequest:
        timestamp = str(int(time()))
        return BoltRequest(
            body=raw_body, headers=self.build_headers(timestamp, raw_body)
        )

    def test_success(self):
        app = App(
            client=self.web_client,
            authorize=authorize,
            signing_secret=self.signing_secret,
        )
        app.action("a")(simple_listener)

        request = self.build_valid_request()
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ""
        assert self.mock_received_requests["/auth.test"] == 1

    def test_failure(self):
        app = App(
            client=self.web_client,
            authorize=error_authorize,
            signing_secret=self.signing_secret,
        )
        app.action("a")(simple_listener)

        request = self.build_valid_request()
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ":x: Please install this app into the workspace :bow:"
        assert self.mock_received_requests.get("/auth.test") == None


body = {
    "type": "block_actions",
    "user": {
        "id": "W111",
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

raw_body = f"payload={quote(json.dumps(body))}"


def simple_listener(ack, body, payload, action):
    assert body["trigger_id"] == "111.222.valid"
    assert body["actions"][0] == payload
    assert payload == action
    assert action["action_id"] == "a"
    ack()
