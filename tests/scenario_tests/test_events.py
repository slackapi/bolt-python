import json
from time import time, sleep

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt import App, BoltRequest
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestEvents:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
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
            "content-type": ["application/json"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    valid_event_body = {
        "token": "verification_token",
        "team_id": "T111",
        "enterprise_id": "E111",
        "api_app_id": "A111",
        "event": {
            "client_msg_id": "9cbd4c5b-7ddf-4ede-b479-ad21fca66d63",
            "type": "app_mention",
            "text": "<@W111> Hi there!",
            "user": "W222",
            "ts": "1595926230.009600",
            "team": "T111",
            "channel": "C111",
            "event_ts": "1595926230.009600",
        },
        "type": "event_callback",
        "event_id": "Ev111",
        "event_time": 1595926230,
        "authed_users": ["W111"],
    }

    def test_mock_server_is_running(self):
        resp = self.web_client.api_test()
        assert resp != None

    def test_middleware(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)

        @app.event("app_mention")
        def handle_app_mention(body, say, payload, event):
            assert body == self.valid_event_body
            assert body["event"] == payload
            assert payload == event
            say("What's up?")

        timestamp, body = str(int(time())), json.dumps(self.valid_event_body)
        request: BoltRequest = BoltRequest(
            body=body, headers=self.build_headers(timestamp, body)
        )
        response = app.dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1
        sleep(1)  # wait a bit after auto ack()
        assert self.mock_received_requests["/chat.postMessage"] == 1

    def test_middleware_skip(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)

        def skip_middleware(req, resp, next):
            # return next()
            pass

        @app.event("app_mention", middleware=[skip_middleware])
        def handle_app_mention(body, logger, payload, event):
            assert body["event"] == payload
            assert payload == event
            logger.info(payload)

        timestamp, body = str(int(time())), json.dumps(self.valid_event_body)
        request: BoltRequest = BoltRequest(
            body=body, headers=self.build_headers(timestamp, body)
        )
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1
