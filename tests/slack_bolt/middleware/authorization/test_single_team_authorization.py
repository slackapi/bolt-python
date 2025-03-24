from slack_sdk import WebClient
from slack_sdk.web import SlackResponse

from slack_bolt.middleware import SingleTeamAuthorization
from slack_bolt.middleware.authorization.internals import _build_user_facing_authorize_error_message
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)


def next():
    return BoltResponse(status=200)


class TestSingleTeamAuthorization:
    mock_api_server_base_url = "http://localhost:8888"

    def setup_method(self):
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)

    def test_success_pattern(self):
        authorization = SingleTeamAuthorization(auth_test_result={})
        req = BoltRequest(body="payload={}", headers={})
        req.context["client"] = WebClient(base_url=self.mock_api_server_base_url, token="xoxb-valid")
        resp = BoltResponse(status=404)

        resp = authorization.process(req=req, resp=resp, next=next)

        assert resp.status == 200
        assert resp.body == ""

    def test_success_pattern_with_bot_scopes(self):
        client = WebClient(base_url=self.mock_api_server_base_url, token="xoxb-valid")
        auth_test_result: SlackResponse = SlackResponse(
            client=client,
            http_verb="POST",
            api_url="https://api.slack.com/api/auth.test",
            req_args={},
            data={},
            headers={"x-oauth-scopes": "chat:write,commands"},
            status_code=200,
        )
        authorization = SingleTeamAuthorization(auth_test_result=auth_test_result)
        req = BoltRequest(body="payload={}", headers={})
        req.context["client"] = client
        resp = BoltResponse(status=404)

        resp = authorization.process(req=req, resp=resp, next=next)

        assert resp.status == 200
        assert resp.body == ""
        assert req.context.authorize_result.bot_scopes == ["chat:write", "commands"]
        assert req.context.authorize_result.user_scopes is None

    def test_failure_pattern(self):
        authorization = SingleTeamAuthorization(auth_test_result={})
        req = BoltRequest(body="payload={}", headers={})
        req.context["client"] = WebClient(base_url=self.mock_api_server_base_url, token="dummy")
        resp = BoltResponse(status=404)

        resp = authorization.process(req=req, resp=resp, next=next)

        assert resp.status == 200
        assert resp.body == _build_user_facing_authorize_error_message()

    def test_failure_pattern_custom_message(self):
        authorization = SingleTeamAuthorization(auth_test_result={}, user_facing_authorize_error_message="foo")
        req = BoltRequest(body="payload={}", headers={})
        req.context["client"] = WebClient(base_url=self.mock_api_server_base_url, token="dummy")
        resp = BoltResponse(status=404)

        resp = authorization.process(req=req, resp=resp, next=next)

        assert resp.status == 200
        assert resp.body == "foo"
