from unittest.mock import MagicMock

import pytest
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_chat_stream import AsyncChatStream

from slack_bolt.context.say_stream.async_say_stream import AsyncSayStream


# TODO: VALIDATE THIS AI SLOP IS CORRECT
def _make_async_chat_stream_mock():
    mock_stream = MagicMock(spec=AsyncChatStream)
    call_tracker = MagicMock()

    async def fake_chat_stream(**kwargs):
        call_tracker(**kwargs)
        return mock_stream

    return fake_chat_stream, call_tracker, mock_stream


class TestAsyncSayStream:
    @pytest.mark.asyncio
    async def test_uses_context_defaults(self):
        client = MagicMock(spec=AsyncWebClient)
        client.chat_stream, call_tracker, _ = _make_async_chat_stream_mock()

        say_stream = AsyncSayStream(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        stream = await say_stream()

        call_tracker.assert_called_once_with(
            channel="C111",
            thread_ts="1234567890.123456",
            recipient_team_id="T111",
            recipient_user_id="W222",
        )
        assert stream is not None

    @pytest.mark.asyncio
    async def test_overrides_context_defaults(self):
        client = MagicMock(spec=AsyncWebClient)
        client.chat_stream, call_tracker, _ = _make_async_chat_stream_mock()

        say_stream = AsyncSayStream(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        stream = await say_stream(
            channel="C999",
            thread_ts="9999999999.999999",
            recipient_team_id="T999",
            recipient_user_id="U999",
        )

        call_tracker.assert_called_once_with(
            channel="C999",
            thread_ts="9999999999.999999",
            recipient_team_id="T999",
            recipient_user_id="U999",
        )
        assert stream is not None

    @pytest.mark.asyncio
    async def test_rejects_partial_overrides(self):
        client = MagicMock(spec=AsyncWebClient)
        say_stream = AsyncSayStream(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        with pytest.raises(ValueError, match="Either provide all of"):
            await say_stream(channel="C999")

    @pytest.mark.asyncio
    async def test_passes_extra_kwargs(self):
        client = MagicMock(spec=AsyncWebClient)
        client.chat_stream, call_tracker, _ = _make_async_chat_stream_mock()

        say_stream = AsyncSayStream(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        await say_stream(buffer_size=512)

        call_tracker.assert_called_once_with(
            channel="C111",
            thread_ts="1234567890.123456",
            recipient_team_id="T111",
            recipient_user_id="W222",
            buffer_size=512,
        )

    @pytest.mark.asyncio
    async def test_raises_without_channel_id(self):
        client = MagicMock(spec=AsyncWebClient)
        say_stream = AsyncSayStream(client=client, channel_id=None, thread_ts="1234567890.123456")
        with pytest.raises(ValueError, match="no channel_id"):
            await say_stream()

    @pytest.mark.asyncio
    async def test_raises_without_thread_ts(self):
        client = MagicMock(spec=AsyncWebClient)
        say_stream = AsyncSayStream(client=client, channel_id="C111", thread_ts=None)
        with pytest.raises(ValueError, match="no thread_ts"):
            await say_stream()
