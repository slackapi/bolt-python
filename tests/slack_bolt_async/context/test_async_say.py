import asyncio

import pytest
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse

from slack_bolt.context.say.async_say import AsyncSay
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)


class TestAsyncSay:
    @pytest.fixture
    def event_loop(self):
        setup_mock_web_api_server(self)
        valid_token = "xoxb-valid"
        mock_api_server_base_url = "http://localhost:8888"
        self.web_client = AsyncWebClient(
            token=valid_token, base_url=mock_api_server_base_url
        )

        loop = asyncio.get_event_loop()
        yield loop
        loop.close()
        cleanup_mock_web_api_server(self)

    @pytest.mark.asyncio
    async def test_say(self):
        say = AsyncSay(client=self.web_client, channel="C111")
        response: AsyncSlackResponse = await say(text="Hi there!")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_say_dict(self):
        say = AsyncSay(client=self.web_client, channel="C111")
        response: AsyncSlackResponse = await say({"text": "Hi!"})
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_say_dict_channel(self):
        say = AsyncSay(client=self.web_client, channel="C111")
        response: AsyncSlackResponse = await say({"text": "Hi!", "channel": "C111"})
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_say_invalid(self):
        say = AsyncSay(client=self.web_client, channel="C111")
        with pytest.raises(ValueError):
            await say([])
