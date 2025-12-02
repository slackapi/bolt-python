import pytest
import asyncio

from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.context.fail.async_fail import AsyncFail
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncFail:
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
    async def test_fail(self):
        fail = AsyncFail(client=self.web_client, function_execution_id="fn1111")

        response = await fail(error="something went wrong")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_fail_no_function_execution_id(self):
        fail = AsyncFail(client=self.web_client, function_execution_id=None)

        with pytest.raises(ValueError):
            await fail(error="there was an error")

    @pytest.mark.asyncio
    async def test_has_been_called_false_initially(self):
        fail = AsyncFail(client=self.web_client, function_execution_id="fn1111")
        assert fail.has_been_called() is False

    @pytest.mark.asyncio
    async def test_has_been_called_true_after_fail(self):
        fail = AsyncFail(client=self.web_client, function_execution_id="fn1111")
        await fail(error="there was an error")
        assert fail.has_been_called() is True
