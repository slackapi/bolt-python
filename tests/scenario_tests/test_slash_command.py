import json
import unittest
from time import time

from slack_bolt.app import App
from slack_bolt.request import BoltRequest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient
from tests.mock_web_api_server import \
    setup_mock_web_api_server, cleanup_mock_web_api_server


class TestSlashCommand(unittest.TestCase):
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = WebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )

    def setUp(self):
        setup_mock_web_api_server(self)

    def tearDown(self):
        cleanup_mock_web_api_server(self)

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
        timestamp, body = str(int(time())), json.dumps(slash_command_payload)
        return BoltRequest(body=body, headers=self.build_headers(timestamp, body))

    def test_mock_server_is_running(self):
        resp = self.web_client.api_test()
        assert resp != None

    def test_success(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.command("/hello-world")(commander)

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
        app.command("/hello-world")(commander)

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

        app.command("/another-one")(commander)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 2


slash_command_payload = \
    "token=verification_token" \
    "&team_id=T111" \
    "&team_domain=test-domain" \
    "&channel_id=C111" \
    "&channel_name=random" \
    "&user_id=W111" \
    "&user_name=primary-owner" \
    "&command=%2Fhello-world" \
    "&text=Hi" \
    "&enterprise_id=E111" \
    "&enterprise_name=Org+Name" \
    "&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT111%2F111%2Fxxxxx" \
    "&trigger_id=111.111.xxx"


def commander(ack):
    ack()
