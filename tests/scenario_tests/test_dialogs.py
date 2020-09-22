import json
from time import time
from urllib.parse import quote

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt.app import App
from slack_bolt.request import BoltRequest
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAttachmentActions:
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
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def build_valid_request(self, body) -> BoltRequest:
        timestamp = str(int(time()))
        return BoltRequest(body=body, headers=self.build_headers(timestamp, body))

    def test_mock_server_is_running(self):
        resp = self.web_client.api_test()
        assert resp != None

    def test_success_without_type(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret,)
        app.options("dialog-callback-id")(handle_suggestion)
        app.action("dialog-callback-id")(handle_submission_cancellation)

        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body != ""
        assert response.headers["content-type"][0] == "application/json;charset=utf-8"
        assert self.mock_received_requests["/auth.test"] == 1

        request = self.build_valid_request(submission_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ""
        assert self.mock_received_requests["/auth.test"] == 1

        request = self.build_valid_request(cancellation_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ""
        assert self.mock_received_requests["/auth.test"] == 1

    def test_success(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret,)
        app.options({"type": "dialog_suggestion", "callback_id": "dialog-callback-id"})(
            handle_suggestion
        )
        app.action({"type": "dialog_submission", "callback_id": "dialog-callback-id"})(
            handle_submission
        )
        app.action(
            {"type": "dialog_cancellation", "callback_id": "dialog-callback-id"}
        )(handle_cancellation)

        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body != ""
        assert response.headers["content-type"][0] == "application/json;charset=utf-8"
        assert self.mock_received_requests["/auth.test"] == 1

        request = self.build_valid_request(submission_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ""
        assert self.mock_received_requests["/auth.test"] == 1

        request = self.build_valid_request(cancellation_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ""
        assert self.mock_received_requests["/auth.test"] == 1

    def test_success_2(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret,)
        app.dialog_suggestion("dialog-callback-id")(handle_suggestion)
        app.dialog_submission("dialog-callback-id")(handle_submission)
        app.dialog_cancellation("dialog-callback-id")(handle_cancellation)

        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body != ""
        assert response.headers["content-type"][0] == "application/json;charset=utf-8"
        assert self.mock_received_requests["/auth.test"] == 1

        request = self.build_valid_request(submission_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ""
        assert self.mock_received_requests["/auth.test"] == 1

        request = self.build_valid_request(cancellation_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ""
        assert self.mock_received_requests["/auth.test"] == 1

    def test_process_before_response(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
            process_before_response=True,
        )
        app.options({"type": "dialog_suggestion", "callback_id": "dialog-callback-id"})(
            handle_suggestion
        )
        app.action({"type": "dialog_submission", "callback_id": "dialog-callback-id"})(
            handle_submission
        )
        app.action(
            {"type": "dialog_cancellation", "callback_id": "dialog-callback-id"}
        )(handle_cancellation)

        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body != ""
        assert response.headers["content-type"][0] == "application/json;charset=utf-8"
        assert self.mock_received_requests["/auth.test"] == 1

        request = self.build_valid_request(submission_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ""
        assert self.mock_received_requests["/auth.test"] == 1

        request = self.build_valid_request(cancellation_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ""
        assert self.mock_received_requests["/auth.test"] == 1

    def test_process_before_response_2(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
            process_before_response=True,
        )
        app.dialog_suggestion("dialog-callback-id")(handle_suggestion)
        app.dialog_submission("dialog-callback-id")(handle_submission)
        app.dialog_cancellation("dialog-callback-id")(handle_cancellation)

        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == json.dumps(options_response)
        assert response.headers["content-type"][0] == "application/json;charset=utf-8"
        assert self.mock_received_requests["/auth.test"] == 1

        request = self.build_valid_request(submission_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ""
        assert self.mock_received_requests["/auth.test"] == 1

        request = self.build_valid_request(cancellation_raw_body)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ""
        assert self.mock_received_requests["/auth.test"] == 1

    def test_suggestion_failure_without_type(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret,)
        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

        app.options("dialog-callback-iddddd")(handle_suggestion)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

    def test_suggestion_failure(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret,)
        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

        app.dialog_suggestion("dialog-callback-iddddd")(handle_suggestion)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

    def test_suggestion_failure_2(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret,)
        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

        app.options(
            {"type": "dialog_suggestion", "callback_id": "dialog-callback-iddddd"}
        )(handle_suggestion)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

    def test_submission_failure_without_type(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret,)
        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

        app.action("dialog-callback-iddddd")(handle_submission)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

    def test_submission_failure(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret,)
        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

        app.dialog_submission("dialog-callback-iddddd")(handle_submission)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

    def test_submission_failure_2(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret,)
        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

        app.action(
            {"type": "dialog_submission", "callback_id": "dialog-callback-iddddd"}
        )(handle_submission)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

    def test_cancellation_failure_without_type(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret,)
        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

        app.action("dialog-callback-iddddd")(handle_cancellation)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

    def test_cancellation_failure(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret,)
        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

        app.dialog_cancellation("dialog-callback-iddddd")(handle_cancellation)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

    def test_cancellation_failure_2(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret,)
        request = self.build_valid_request(suggestion_raw_body)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

        app.action(
            {"type": "dialog_cancellation", "callback_id": "dialog-callback-iddddd"}
        )(handle_cancellation)
        response = app.dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1


suggestion_body = {
    "type": "dialog_suggestion",
    "token": "verification_token",
    "action_ts": "1596603332.676855",
    "team": {
        "id": "T111",
        "domain": "workspace-domain",
        "enterprise_id": "E111",
        "enterprise_name": "Sandbox Org",
    },
    "user": {"id": "W111", "name": "primary-owner", "team_id": "T111"},
    "channel": {"id": "C111", "name": "test-channel"},
    "name": "types",
    "value": "search keyword",
    "callback_id": "dialog-callback-id",
    "state": "Limo",
}

submission_body = {
    "type": "dialog_submission",
    "token": "verification_token",
    "action_ts": "1596603334.328193",
    "team": {
        "id": "T111",
        "domain": "workspace-domain",
        "enterprise_id": "E111",
        "enterprise_name": "Sandbox Org",
    },
    "user": {"id": "W111", "name": "primary-owner", "team_id": "T111"},
    "channel": {"id": "C111", "name": "test-channel"},
    "submission": {
        "loc_origin": "Tokyo",
        "loc_destination": "Osaka",
        "types": "FE-459",
    },
    "callback_id": "dialog-callback-id",
    "response_url": "https://hooks.slack.com/app/T111/111/xxx",
    "state": "Limo",
}

cancellation_body = {
    "type": "dialog_cancellation",
    "token": "verification_token",
    "action_ts": "1596603453.047897",
    "team": {
        "id": "T111",
        "domain": "workspace-domain",
        "enterprise_id": "E111",
        "enterprise_name": "Sandbox Org",
    },
    "user": {"id": "W111", "name": "primary-owner", "team_id": "T111"},
    "channel": {"id": "C111", "name": "test-channel"},
    "callback_id": "dialog-callback-id",
    "response_url": "https://hooks.slack.com/app/T111/111/xxx",
    "state": "Limo",
}

suggestion_raw_body = f"payload={quote(json.dumps(suggestion_body))}"
submission_raw_body = f"payload={quote(json.dumps(submission_body))}"
cancellation_raw_body = f"payload={quote(json.dumps(cancellation_body))}"


def handle_submission(ack):
    ack()


options_response = {
    "options": [
        {
            "label": "[UXD-342] The button color should be artichoke green, not jalapeño",
            "value": "UXD-342",
        },
        {"label": "[FE-459] Remove the marquee tag", "value": "FE-459"},
        {"label": "[FE-238] Too many shades of gray in master CSS", "value": "FE-238",},
    ]
}


def handle_suggestion(ack, body, payload, options):
    assert body == options
    assert payload == options
    ack(options_response)


def handle_cancellation(ack, body, payload, action):
    assert body == action
    assert payload == action
    ack()


def handle_submission_cancellation(ack, body, payload, action):
    assert body == action
    assert payload == action
    ack()
