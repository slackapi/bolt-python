from unittest.mock import MagicMock, patch

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

    def test_set_suggested_prompts_without_thread_ts(self):
        set_suggested_prompts = SetSuggestedPrompts(client=self.web_client, channel_id="C111")
        with patch.object(
            self.web_client, self.web_client.assistant_threads_setSuggestedPrompts.__name__, return_value=MagicMock()
        ) as mock_api:
            set_suggested_prompts(prompts=["One", "Two"])
            mock_api.assert_called_once_with(
                channel_id="C111",
                thread_ts=None,
                prompts=[{"title": "One", "message": "One"}, {"title": "Two", "message": "Two"}],
                title=None,
            )

    def test_set_suggested_prompts_thread_ts_override(self):
        # The call-time thread_ts must win over the stored one
        set_suggested_prompts = SetSuggestedPrompts(client=self.web_client, channel_id="C111", thread_ts="999.999")
        with patch.object(
            self.web_client, self.web_client.assistant_threads_setSuggestedPrompts.__name__, return_value=MagicMock()
        ) as mock_api:
            set_suggested_prompts(prompts=["One", "Two"], thread_ts="123.123")
            mock_api.assert_called_once_with(
                channel_id="C111",
                thread_ts="123.123",
                prompts=[{"title": "One", "message": "One"}, {"title": "Two", "message": "Two"}],
                title=None,
            )

    def test_set_suggested_prompts_thread_ts_override_falsy(self):
        # An explicitly passed falsy thread_ts must be forwarded, not swallowed by the stored value
        set_suggested_prompts = SetSuggestedPrompts(client=self.web_client, channel_id="C111", thread_ts="123.123")
        with patch.object(
            self.web_client, self.web_client.assistant_threads_setSuggestedPrompts.__name__, return_value=MagicMock()
        ) as mock_api:
            set_suggested_prompts(prompts=["One", "Two"], thread_ts="")
            mock_api.assert_called_once_with(
                channel_id="C111",
                thread_ts="",
                prompts=[{"title": "One", "message": "One"}, {"title": "Two", "message": "Two"}],
                title=None,
            )

    def test_set_suggested_prompts_invalid(self):
        set_suggested_prompts = SetSuggestedPrompts(client=self.web_client, channel_id="C111", thread_ts="123.123")
        with pytest.raises(TypeError):
            set_suggested_prompts()
