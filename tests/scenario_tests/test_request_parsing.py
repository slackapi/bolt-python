import json
from time import time

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt import App, BoltRequest
from tests.mock_web_api_server import cleanup_mock_web_api_server, setup_mock_web_api_server
from tests.scenario_tests import test_block_actions, test_shortcut, test_slash_command, test_view_submission
from tests.slack_bolt.request import test_internals
from tests.utils import remove_os_env_temporarily, restore_os_env

form_bodies = [
    test_block_actions.raw_body,
    test_shortcut.global_shortcut_raw_body,
    test_shortcut.message_shortcut_raw_body,
    test_slash_command.slash_command_body,
    test_view_submission.raw_body,
    test_view_submission.raw_response_url_body,
    test_view_submission.connect_channel_body,
]
json_bodies = [
    json.dumps(payload)
    for name, payloads in vars(test_internals.TestRequestInternals).items()
    if name.endswith("requests")
    for payload in payloads
]
signed_bodies = form_bodies + json_bodies

malformed_unsigned_bodies = [
    json.dumps(
        {
            "type": "event_callback",
            "event": {"type": "member_joined_channel", "user": "U0123456789", "channel": "C0123456789"},
        }
    ),
    '{"type": "event_callback", "event": ',
    "[1, 2, 3]",
    json.dumps({"user": "U0123456789", "view": "V0123456789", "enterprise": 1}),
]


def plain_values(context: dict) -> dict:
    return {
        key: value if isinstance(value, (str, bool, int, dict, list, type(None))) else type(value).__name__
        for key, value in context.items()
    }


class TestRequestParsing:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = WebClient(token=valid_token, base_url=mock_api_server_base_url)

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    def build_request(self, body: str, defer_parsing: bool) -> BoltRequest:
        timestamp = str(int(time()))
        content_type = "application/json" if body.startswith("{") else "application/x-www-form-urlencoded"
        return BoltRequest(
            body=body,
            headers={
                "content-type": [content_type],
                "x-slack-signature": [self.signature_verifier.generate_signature(body=body, timestamp=timestamp)],
                "x-slack-request-timestamp": [timestamp],
            },
            defer_parsing=defer_parsing,
        )

    def capture_after_dispatch(self, request: BoltRequest) -> dict:
        app = App(client=self.web_client, signing_secret=self.signing_secret)
        captured = {}

        @app.middleware
        def capture(context, body, next):
            captured["context"] = plain_values(context)
            captured["body"] = body
            captured["client_default_params"] = dict(context.client.default_params)
            next()

        app.dispatch(request)
        return captured

    def test_deferred_parsing_matches_eager_parsing(self):
        for body in signed_bodies:
            eager = self.capture_after_dispatch(self.build_request(body, defer_parsing=False))
            deferred = self.capture_after_dispatch(self.build_request(body, defer_parsing=True))
            assert eager != {}
            assert deferred == eager, body

    def test_deferred_request_is_unparsed_until_dispatch(self):
        request = self.build_request(test_slash_command.slash_command_body, defer_parsing=True)
        assert request.body == {}
        assert request.context.team_id is None
        request.complete_deferred_parsing()
        assert request.body["team_id"] == "T111"
        assert request.context.team_id == "T111"

    def test_context_set_after_creation_wins_over_body(self):
        request = self.build_request(test_slash_command.slash_command_body, defer_parsing=True)
        request.context["team_id"] = "T_FROM_ADAPTER"
        request.context["lambda_request"] = {"source": "adapter"}
        request.complete_deferred_parsing()
        assert request.context.team_id == "T_FROM_ADAPTER"
        assert request.context["lambda_request"] == {"source": "adapter"}
        assert request.context.user_id == "W111"

    def test_malformed_unsigned_deferred_requests_are_rejected(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)
        for body in malformed_unsigned_bodies:
            request = BoltRequest(body=body, headers={"content-type": ["application/json"]}, defer_parsing=True)
            assert app.dispatch(request).status == 401

    def test_deferred_parsing_without_request_verification(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret, request_verification_enabled=False)
        captured = {}

        @app.middleware
        def capture(context, next):
            captured["team_id"] = context.team_id
            next()

        request = BoltRequest(body=test_slash_command.slash_command_body, defer_parsing=True)
        app.dispatch(request)
        assert captured["team_id"] == "T111"

    def test_signed_invalid_json_is_handled_by_the_error_handler(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)
        response = app.dispatch(self.build_request('{"type": "event_callback", ', defer_parsing=True))
        assert response.status == 500

    def test_ssl_check_on_deferred_request(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)
        request = BoltRequest(body="token=random&ssl_check=1", defer_parsing=True)
        response = app.dispatch(request)
        assert response.status == 200
        assert response.body == ""

    def test_to_copyable_of_deferred_request_is_parsed(self):
        request = self.build_request(test_slash_command.slash_command_body, defer_parsing=True)
        request.complete_deferred_parsing()
        copied = request.to_copyable()
        assert copied.defer_parsing is False
        assert copied.body == request.body
        assert copied.context.team_id == "T111"
