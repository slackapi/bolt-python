from email import message
import pytest

from slack_sdk import WebClient
from slack_bolt.context.complete_error import CompleteError
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)


class TestCompleteError:
    def setup_method(self):
        setup_mock_web_api_server(self)
        valid_token = "xoxb-valid"
        mock_api_server_base_url = "http://localhost:8888"
        self.web_client = WebClient(token=valid_token, base_url=mock_api_server_base_url)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)

    def test_complete_error(self):
        complete_error = CompleteError(client=self.web_client, function_execution_id="fn1111")

        response = complete_error(message="something went wrong")

        assert response.status_code == 200

    def test_complete_error_invalid_args(self):
        complete_error = CompleteError(client=self.web_client, function_execution_id="fn1111")

        with pytest.raises(ValueError):
            complete_error([])

    def test_complete_error_invalid_id(self):
        complete_error = CompleteError(client=self.web_client, function_execution_id=None)

        with pytest.raises(ValueError):
            complete_error(message="something went wrong")
