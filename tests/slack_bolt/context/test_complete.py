import pytest

from slack_sdk import WebClient
from slack_bolt.context.complete import Complete
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)


class TestComplete:
    def setup_method(self):
        setup_mock_web_api_server(self)
        valid_token = "xoxb-valid"
        mock_api_server_base_url = "http://localhost:8888"
        self.web_client = WebClient(token=valid_token, base_url=mock_api_server_base_url)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)

    def test_complete(self):
        complete_success = Complete(client=self.web_client, function_execution_id="fn1111")

        response = complete_success(outputs={"key": "value"})

        assert response.status_code == 200

    def test_complete_no_function_execution_id(self):
        complete = Complete(client=self.web_client, function_execution_id=None)

        with pytest.raises(ValueError):
            complete(outputs={"key": "value"})
