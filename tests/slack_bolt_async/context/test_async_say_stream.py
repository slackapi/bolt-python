import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.context.say_stream.async_say_stream import AsyncSayStream
from slack_bolt.warning import ExperimentalWarning
from tests.mock_web_api_server import (
    cleanup_mock_web_api_server,
    setup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncSayStream:
    default_chat_stream_buffer_size = AsyncWebClient.chat_stream.__kwdefaults__["buffer_size"]

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
    async def test_missing_channel_raises(self):
        say_stream = AsyncSayStream(client=self.web_client, channel=None, thread_ts="111.222")
        with pytest.warns(ExperimentalWarning):
            with pytest.raises(ValueError, match="channel"):
                await say_stream()

    @pytest.mark.asyncio
    async def test_missing_thread_ts_raises(self):
        say_stream = AsyncSayStream(client=self.web_client, channel="C111", thread_ts=None)
        with pytest.warns(ExperimentalWarning):
            with pytest.raises(ValueError, match="thread_ts"):
                await say_stream()

    @pytest.mark.asyncio
    async def test_default_params(self):
        say_stream = AsyncSayStream(
            client=self.web_client,
            channel="C111",
            recipient_team_id="T111",
            recipient_user_id="U111",
            thread_ts="111.222",
        )
        stream = await say_stream()

        assert stream._buffer_size == self.default_chat_stream_buffer_size
        assert stream._stream_args == {
            "channel": "C111",
            "thread_ts": "111.222",
            "recipient_team_id": "T111",
            "recipient_user_id": "U111",
            "task_display_mode": None,
        }

    @pytest.mark.asyncio
    async def test_parameter_overrides(self):
        say_stream = AsyncSayStream(
            client=self.web_client,
            channel="C111",
            recipient_team_id="T111",
            recipient_user_id="U111",
            thread_ts="111.222",
        )
        stream = await say_stream(channel="C222", thread_ts="333.444", recipient_team_id="T222", recipient_user_id="U222")

        assert stream._buffer_size == self.default_chat_stream_buffer_size
        assert stream._stream_args == {
            "channel": "C222",
            "thread_ts": "333.444",
            "recipient_team_id": "T222",
            "recipient_user_id": "U222",
            "task_display_mode": None,
        }

    @pytest.mark.asyncio
    async def test_buffer_size_overrides(self):
        say_stream = AsyncSayStream(
            client=self.web_client,
            channel="C111",
            recipient_team_id="T111",
            recipient_user_id="U111",
            thread_ts="111.222",
        )
        stream = await say_stream(
            buffer_size=100,
            channel="C222",
            thread_ts="333.444",
            recipient_team_id="T222",
            recipient_user_id="U222",
        )

        assert stream._buffer_size == 100
        assert stream._stream_args == {
            "channel": "C222",
            "thread_ts": "333.444",
            "recipient_team_id": "T222",
            "recipient_user_id": "U222",
            "task_display_mode": None,
        }

    @pytest.mark.asyncio
    async def test_experimental_warning(self):
        say_stream = AsyncSayStream(
            client=self.web_client,
            channel="C111",
            thread_ts="111.222",
        )
        with pytest.warns(ExperimentalWarning, match="say_stream is experimental"):
            await say_stream()
