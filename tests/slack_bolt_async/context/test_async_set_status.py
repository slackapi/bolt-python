import pytest
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse

from slack_bolt.context.set_status.async_set_status import AsyncSetStatus
from tests.mock_web_api_server import cleanup_mock_web_api_server_async, setup_mock_web_api_server_async
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncSetStatus:

    @pytest.fixture(scope="function", autouse=True)
    def setup_teardown(self):
        old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server_async(self)
        valid_token = "xoxb-valid"
        mock_api_server_base_url = "http://localhost:8888"
        try:
            self.web_client = AsyncWebClient(token=valid_token, base_url=mock_api_server_base_url)
            yield  # run the test here
        finally:
            cleanup_mock_web_api_server_async(self)
            restore_os_env(old_os_env)

    @pytest.mark.asyncio
    async def test_set_status(self):
        set_status = AsyncSetStatus(client=self.web_client, channel_id="C111", thread_ts="123.123")
        response: AsyncSlackResponse = await set_status("Thinking...")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_set_status_loading_messages(self):
        set_status = AsyncSetStatus(client=self.web_client, channel_id="C111", thread_ts="123.123")
        response: AsyncSlackResponse = await set_status(
            status="Thinking...",
            loading_messages=[
                "Sitting...",
                "Waiting...",
            ],
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_set_status_invalid(self):
        set_status = AsyncSetStatus(client=self.web_client, channel_id="C111", thread_ts="123.123")
        with pytest.raises(TypeError):
            await set_status()
