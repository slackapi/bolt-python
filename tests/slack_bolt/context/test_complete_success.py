from slack_sdk import WebClient
from slack_bolt.context.complete_success.complete_success import CompleteSuccess
from slack_bolt.context.respond import Respond
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)


class TestCompleteSuccess:
    def setup_method(self):
        setup_mock_web_api_server(self)
        valid_token = "xoxb-valid"
        mock_api_server_base_url = "http://localhost:8888"
        self.web_client = WebClient(token=valid_token, base_url=mock_api_server_base_url)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)

    def test_complete_success(self):
        # given
        complete_success = CompleteSuccess(self.web_client, "fn1111")

        # when
        response = complete_success(outputs={"key": "value"})

        # then
        assert response.status_code == 200

    def test_respond2(self):
        response_url = "http://localhost:8888"
        respond = Respond(response_url=response_url)
        response = respond({"text": "Hi there!"})
        assert response.status_code == 200

    def test_unfurl_options(self):
        response_url = "http://localhost:8888"
        respond = Respond(response_url=response_url)
        response = respond(text="Hi there!", unfurl_media=True, unfurl_links=True)
        assert response.status_code == 200
