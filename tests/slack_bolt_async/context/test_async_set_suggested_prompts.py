import asyncio

import pytest
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse

from slack_bolt.context.set_suggested_prompts.async_set_suggested_prompts import AsyncSetSuggestedPrompts
from tests.mock_web_api_server import cleanup_mock_web_api_server, setup_mock_web_api_server


class TestAsyncSetSuggestedPrompts:
    @pytest.fixture
    def event_loop(self):
        setup_mock_web_api_server(self)
        valid_token = "xoxb-valid"
        mock_api_server_base_url = "http://localhost:8888"
        self.web_client = AsyncWebClient(token=valid_token, base_url=mock_api_server_base_url)

        loop = asyncio.get_event_loop()
        yield loop
        loop.close()
        cleanup_mock_web_api_server(self)

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
    async def test_set_suggested_prompts_invalid(self):
        set_suggested_prompts = AsyncSetSuggestedPrompts(client=self.web_client, channel_id="C111", thread_ts="123.123")
        with pytest.raises(TypeError):
            await set_suggested_prompts()
