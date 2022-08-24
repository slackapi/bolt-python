import asyncio
import pytest

from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.context.complete_error.async_complete_error import AsyncCompleteError
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)


class TestAsyncCompleteError:
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
    async def test_complete_error(self):
        complete_error = AsyncCompleteError(client=self.web_client, function_execution_id="fn1111")

        response = await complete_error(message="something went wrong")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_complete_error_invalid_args(self):
        complete_error = AsyncCompleteError(client=self.web_client, function_execution_id="fn1111")

        with pytest.raises(ValueError):
            await complete_error([])

    @pytest.mark.asyncio
    async def test_complete_error_invalid_id(self):
        complete_error = AsyncCompleteError(client=self.web_client, function_execution_id=None)

        with pytest.raises(ValueError):
            await complete_error(message="something went wrong")
