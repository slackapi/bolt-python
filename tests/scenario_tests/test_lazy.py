import json
import time
from urllib.parse import quote

from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier

from slack_bolt import BoltRequest
from slack_bolt.app import App
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestErrorHandler:
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

    # ----------------
    #  utilities
    # ----------------

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

    def build_valid_request(self) -> BoltRequest:
        body = {
            "type": "block_actions",
            "user": {
                "id": "W111",
            },
            "api_app_id": "A111",
            "token": "verification_token",
            "trigger_id": "111.222.valid",
            "team": {
                "id": "T111",
            },
            "channel": {"id": "C111", "name": "test-channel"},
            "response_url": "https://hooks.slack.com/actions/T111/111/random-value",
            "actions": [
                {
                    "action_id": "a",
                    "block_id": "b",
                    "text": {"type": "plain_text", "text": "Button"},
                    "value": "click_me_123",
                    "type": "button",
                    "action_ts": "1596530385.194939",
                }
            ],
        }
        raw_body = f"payload={quote(json.dumps(body))}"
        timestamp = str(int(time.time()))
        return BoltRequest(
            body=raw_body, headers=self.build_headers(timestamp, raw_body)
        )

    # ----------------
    #  tests
    # ----------------

    def test_lazy(self):
        def just_ack(ack):
            ack()

        def async1(say):
            time.sleep(0.3)
            say(text="lazy function 1")

        def async2(say):
            time.sleep(0.5)
            say(text="lazy function 2")

        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.action("a")(
            ack=just_ack,
            lazy=[async1, async2],
        )

        request = self.build_valid_request()
        response = app.dispatch(request)
        assert response.status == 200
        time.sleep(1)  # wait a bit
        assert self.mock_received_requests["/chat.postMessage"] == 2
