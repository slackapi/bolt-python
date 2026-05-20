import pytest
from unittest.mock import patch, MagicMock

from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.context.say_stream.async_say_stream import AsyncSayStream
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncSayStream:
    @pytest.fixture(scope="function", autouse=True)
    def setup_teardown(self):
        old_os_env = remove_os_env_temporarily()
        try:
            self.web_client = AsyncWebClient(token="xoxb-valid")
            yield
        finally:
            restore_os_env(old_os_env)

    @pytest.mark.asyncio
    async def test_missing_channel_raises(self):
        say_stream = AsyncSayStream(client=self.web_client, channel=None, thread_ts="111.222")
        with pytest.raises(ValueError, match="channel"):
            await say_stream()

    @pytest.mark.asyncio
    async def test_missing_thread_ts_raises(self):
        say_stream = AsyncSayStream(client=self.web_client, channel="C111", thread_ts=None)
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
        mock_chat_stream = MagicMock()

        async def fake_chat_stream(**kwargs):
            return mock_chat_stream(**kwargs)

        with patch.object(self.web_client, "chat_stream", side_effect=fake_chat_stream):
            await say_stream()
            mock_chat_stream.assert_called_once_with(
                channel="C111",
                recipient_team_id="T111",
                recipient_user_id="U111",
                thread_ts="111.222",
                icon_emoji=None,
                icon_url=None,
                username=None,
            )

    @pytest.mark.asyncio
    async def test_parameter_overrides(self):
        say_stream = AsyncSayStream(
            client=self.web_client,
            channel="C111",
            recipient_team_id="T111",
            recipient_user_id="U111",
            thread_ts="111.222",
        )
        mock_chat_stream = MagicMock()

        async def fake_chat_stream(**kwargs):
            return mock_chat_stream(**kwargs)

        with patch.object(self.web_client, "chat_stream", side_effect=fake_chat_stream):
            await say_stream(channel="C222", thread_ts="333.444", recipient_team_id="T222", recipient_user_id="U222")
            mock_chat_stream.assert_called_once_with(
                channel="C222",
                recipient_team_id="T222",
                recipient_user_id="U222",
                thread_ts="333.444",
                icon_emoji=None,
                icon_url=None,
                username=None,
            )

    @pytest.mark.asyncio
    async def test_buffer_size_overrides(self):
        say_stream = AsyncSayStream(
            client=self.web_client,
            channel="C111",
            recipient_team_id="T111",
            recipient_user_id="U111",
            thread_ts="111.222",
        )
        mock_chat_stream = MagicMock()

        async def fake_chat_stream(**kwargs):
            return mock_chat_stream(**kwargs)

        with patch.object(self.web_client, "chat_stream", side_effect=fake_chat_stream):
            await say_stream(
                buffer_size=100,
                channel="C222",
                thread_ts="333.444",
                recipient_team_id="T222",
                recipient_user_id="U222",
            )
            mock_chat_stream.assert_called_once_with(
                buffer_size=100,
                channel="C222",
                recipient_team_id="T222",
                recipient_user_id="U222",
                thread_ts="333.444",
                icon_emoji=None,
                icon_url=None,
                username=None,
            )

    @pytest.mark.asyncio
    async def test_authorship_overrides(self):
        say_stream = AsyncSayStream(
            client=self.web_client,
            channel="C111",
            recipient_team_id="T111",
            recipient_user_id="U111",
            thread_ts="111.222",
        )
        mock_chat_stream = MagicMock()

        async def fake_chat_stream(**kwargs):
            return mock_chat_stream(**kwargs)

        with patch.object(self.web_client, "chat_stream", side_effect=fake_chat_stream):
            await say_stream(icon_emoji=":maple_leaf:", username="Charlie Brown")
            mock_chat_stream.assert_called_once_with(
                channel="C111",
                recipient_team_id="T111",
                recipient_user_id="U111",
                thread_ts="111.222",
                icon_emoji=":maple_leaf:",
                icon_url=None,
                username="Charlie Brown",
            )
