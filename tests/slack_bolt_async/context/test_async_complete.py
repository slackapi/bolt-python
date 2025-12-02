import pytest
import asyncio

from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.context.complete.async_complete import AsyncComplete
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncComplete:

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
    async def test_complete(self):
        complete_success = AsyncComplete(client=self.web_client, function_execution_id="fn1111")

        response = await complete_success(outputs={"key": "value"})

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_complete_no_function_execution_id(self):
        complete = AsyncComplete(client=self.web_client, function_execution_id=None)

        with pytest.raises(ValueError):
            await complete(outputs={"key": "value"})

    @pytest.mark.asyncio
    async def test_has_been_called_false_initially(self):
        complete = AsyncComplete(client=self.web_client, function_execution_id="fn1111")
        assert complete.has_been_called() is False

    @pytest.mark.asyncio
    async def test_has_been_called_true_after_complete(self):
        complete = AsyncComplete(client=self.web_client, function_execution_id="fn1111")
        await complete(outputs={"key": "value"})
        assert complete.has_been_called() is True
