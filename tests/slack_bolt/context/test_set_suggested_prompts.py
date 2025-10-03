import pytest
from slack_sdk import WebClient
from slack_sdk.web import SlackResponse

from slack_bolt.context.set_suggested_prompts import SetSuggestedPrompts
from tests.mock_web_api_server import cleanup_mock_web_api_server, setup_mock_web_api_server


class TestSetSuggestedPrompts:
    def setup_method(self):
        setup_mock_web_api_server(self)
        valid_token = "xoxb-valid"
        mock_api_server_base_url = "http://localhost:8888"
        self.web_client = WebClient(token=valid_token, base_url=mock_api_server_base_url)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)

    def test_set_suggested_prompts(self):
        set_suggested_prompts = SetSuggestedPrompts(client=self.web_client, channel_id="C111", thread_ts="123.123")
        response: SlackResponse = set_suggested_prompts(prompts=["One", "Two"])
        assert response.status_code == 200

    def test_set_suggested_prompts_objects(self):
        set_suggested_prompts = SetSuggestedPrompts(client=self.web_client, channel_id="C111", thread_ts="123.123")
        response: SlackResponse = set_suggested_prompts(
            prompts=[
                "One",
                {"title": "Two", "message": "What's before addition?"},
            ],
        )
        assert response.status_code == 200

    def test_set_suggested_prompts_invalid(self):
        set_suggested_prompts = SetSuggestedPrompts(client=self.web_client, channel_id="C111", thread_ts="123.123")
        with pytest.raises(TypeError):
            set_suggested_prompts()
