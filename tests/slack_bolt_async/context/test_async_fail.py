import pytest
import asyncio

from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.context.fail.async_fail import AsyncFail
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)


class TestAsyncFail:
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
    async def test_fail(self):
        fail = AsyncFail(client=self.web_client, function_execution_id="fn1111")

        response = await fail(error="something went wrong")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_fail_no_function_execution_id(self):
        fail = AsyncFail(client=self.web_client, function_execution_id=None)

        with pytest.raises(ValueError):
            await fail(error="there was an error")
