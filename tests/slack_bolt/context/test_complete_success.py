import pytest

from slack_sdk import WebClient
from slack_bolt.context.complete_success import CompleteSuccess
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
        complete_success = CompleteSuccess(client=self.web_client, function_execution_id="fn1111")

        response = complete_success(outputs={"key": "value"})

        assert response.status_code == 200

    def test_complete_success_invalid_outputs(self):
        complete_success = CompleteSuccess(client=self.web_client, function_execution_id="fn1111")

        with pytest.raises(ValueError):
            complete_success([])

    def test_complete_success_invalid_id(self):
        complete_success = CompleteSuccess(client=self.web_client, function_execution_id=None)

        with pytest.raises(ValueError):
            complete_success(outputs={"key": "value"})
