import pytest

from slack_sdk import WebClient
from slack_bolt.context.fail import Fail
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)


class TestFail:
    def setup_method(self):
        setup_mock_web_api_server(self)
        valid_token = "xoxb-valid"
        mock_api_server_base_url = "http://localhost:8888"
        self.web_client = WebClient(token=valid_token, base_url=mock_api_server_base_url)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)

    def test_fail(self):
        fail = Fail(client=self.web_client, function_execution_id="fn1111")

        response = fail(error="something went wrong")

        assert response.status_code == 200

    def test_fail_no_function_execution_id(self):
        fail = Fail(client=self.web_client, function_execution_id=None)

        with pytest.raises(ValueError):
            fail(error="there was an error")
