import asyncio
from unittest.mock import MagicMock, patch

import pytest
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse

from slack_bolt.context.set_suggested_prompts.async_set_suggested_prompts import AsyncSetSuggestedPrompts
from tests.mock_web_api_server import cleanup_mock_web_api_server, setup_mock_web_api_server
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncSetSuggestedPrompts:

    @pytest.fixture(scope="function", autouse=True)
    def setup_teardown(self):
        old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)
        valid_token = "xoxb-valid"
        mock_api_server_base_url = "http://localhost:8888"
        try:
            self.web_client = AsyncWebClient(token=valid_token, base_url=mock_api_server_base_url)
            yield  # run the test here
        finally:
            cleanup_mock_web_api_server(self)
            restore_os_env(old_os_env)

    @pytest.mark.asyncio
    async def test_set_suggested_prompts(self):
        set_suggested_prompts = AsyncSetSuggestedPrompts(client=self.web_client, channel_id="C111", thread_ts="123.123")
        response: AsyncSlackResponse = await set_suggested_prompts(prompts=["One", "Two"])
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_set_suggested_prompts_objects(self):
        set_suggested_prompts = AsyncSetSuggestedPrompts(client=self.web_client, channel_id="C111", thread_ts="123.123")
        response: AsyncSlackResponse = await set_suggested_prompts(
            prompts=[
                "One",
                {"title": "Two", "message": "What's before addition?"},
            ],
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_set_suggested_prompts_without_thread_ts(self):
        set_suggested_prompts = AsyncSetSuggestedPrompts(client=self.web_client, channel_id="C111")
        mock_api = MagicMock()

        async def fake_api(**kwargs):
            return mock_api(**kwargs)

        with patch.object(
            self.web_client, self.web_client.assistant_threads_setSuggestedPrompts.__name__, side_effect=fake_api
        ):
            await set_suggested_prompts(prompts=["One", "Two"])
            mock_api.assert_called_once_with(
                channel_id="C111",
                thread_ts=None,
                prompts=[{"title": "One", "message": "One"}, {"title": "Two", "message": "Two"}],
                title=None,
            )

    @pytest.mark.asyncio
    async def test_set_suggested_prompts_thread_ts_override(self):
        # The call-time thread_ts must win over the stored one
        set_suggested_prompts = AsyncSetSuggestedPrompts(client=self.web_client, channel_id="C111", thread_ts="999.999")
        mock_api = MagicMock()

        async def fake_api(**kwargs):
            return mock_api(**kwargs)

        with patch.object(
            self.web_client, self.web_client.assistant_threads_setSuggestedPrompts.__name__, side_effect=fake_api
        ):
            await set_suggested_prompts(prompts=["One", "Two"], thread_ts="123.123")
            mock_api.assert_called_once_with(
                channel_id="C111",
                thread_ts="123.123",
                prompts=[{"title": "One", "message": "One"}, {"title": "Two", "message": "Two"}],
                title=None,
            )

    @pytest.mark.asyncio
    async def test_set_suggested_prompts_thread_ts_override_falsy(self):
        # An explicitly passed falsy thread_ts must be forwarded, not swallowed by the stored value
        set_suggested_prompts = AsyncSetSuggestedPrompts(client=self.web_client, channel_id="C111", thread_ts="123.123")
        mock_api = MagicMock()

        async def fake_api(**kwargs):
            return mock_api(**kwargs)

        with patch.object(
            self.web_client, self.web_client.assistant_threads_setSuggestedPrompts.__name__, side_effect=fake_api
        ):
            await set_suggested_prompts(prompts=["One", "Two"], thread_ts="")
            mock_api.assert_called_once_with(
                channel_id="C111",
                thread_ts="",
                prompts=[{"title": "One", "message": "One"}, {"title": "Two", "message": "Two"}],
                title=None,
            )

    @pytest.mark.asyncio
    async def test_set_suggested_prompts_invalid(self):
        set_suggested_prompts = AsyncSetSuggestedPrompts(client=self.web_client, channel_id="C111", thread_ts="123.123")
        with pytest.raises(TypeError):
            await set_suggested_prompts()
