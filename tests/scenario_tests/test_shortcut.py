import json
import unittest
from time import time
from urllib.parse import quote

from slack_bolt import BoltRequest
from slack_bolt.app import App
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from tests.mock_web_api_server import \
    setup_mock_web_api_server, cleanup_mock_web_api_server
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestShortcut(unittest.TestCase):
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = WebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )

    def setUp(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def tearDown(self):
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
            "x-slack-request-timestamp": [timestamp]
        }

    def build_valid_request(self) -> BoltRequest:
        timestamp = str(int(time()))
        return BoltRequest(body=raw_body, headers=self.build_headers(timestamp, raw_body))

    def test_mock_server_is_running(self):
        resp = self.web_client.api_test()
        assert resp != None

    def test_success(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.shortcut("test-shortcut")(simple_listener)

        request = self.build_valid_request()
        response = app.dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1

    def test_process_before_response(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
            process_before_response=True,
        )
        app.shortcut("test-shortcut")(simple_listener)

        request = self.build_valid_request()
        response = app.dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1

    def test_failure(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        request = self.build_valid_request()
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

        app.shortcut("another-one")(simple_listener)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 2


payload = {
    "type": "shortcut",
    "token": "verification_token",
    "action_ts": "111.111",
    "team": {
        "id": "T111",
        "domain": "workspace-domain",
        "enterprise_id": "E111",
        "enterprise_name": "Org Name"
    },
    "user": {
        "id": "W111",
        "username": "primary-owner",
        "team_id": "T111"
    },
    "callback_id": "test-shortcut",
    "trigger_id": "111.111.xxxxxx"
}

raw_body = f"payload={quote(json.dumps(payload))}"


def simple_listener(ack):
    ack()
