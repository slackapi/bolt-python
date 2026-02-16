from unittest.mock import MagicMock

import pytest
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_chat_stream import AsyncChatStream

from slack_bolt.agent.async_agent import AsyncBoltAgent


def _make_async_chat_stream_mock():
    mock_stream = MagicMock(spec=AsyncChatStream)
    call_tracker = MagicMock()

    async def fake_chat_stream(**kwargs):
        call_tracker(**kwargs)
        return mock_stream

    return fake_chat_stream, call_tracker, mock_stream


class TestAsyncBoltAgent:
    @pytest.mark.asyncio
    async def test_chat_stream_uses_context_defaults(self):
        """AsyncBoltAgent.chat_stream() passes context defaults to AsyncWebClient.chat_stream()."""
        client = MagicMock(spec=AsyncWebClient)
        client.chat_stream, call_tracker, _ = _make_async_chat_stream_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        stream = await agent.chat_stream()

        call_tracker.assert_called_once_with(
            channel="C111",
            thread_ts="1234567890.123456",
            recipient_team_id="T111",
            recipient_user_id="W222",
        )
        assert stream is not None

    @pytest.mark.asyncio
    async def test_chat_stream_overrides_context_defaults(self):
        """Explicit kwargs to chat_stream() override context defaults."""
        client = MagicMock(spec=AsyncWebClient)
        client.chat_stream, call_tracker, _ = _make_async_chat_stream_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        stream = await agent.chat_stream(
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
    async def test_chat_stream_rejects_partial_overrides(self):
        """Passing only some of the four context args raises ValueError."""
        client = MagicMock(spec=AsyncWebClient)
        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        with pytest.raises(ValueError, match="Either provide all of"):
            await agent.chat_stream(channel="C999")

    @pytest.mark.asyncio
    async def test_chat_stream_passes_extra_kwargs(self):
        """Extra kwargs are forwarded to AsyncWebClient.chat_stream()."""
        client = MagicMock(spec=AsyncWebClient)
        client.chat_stream, call_tracker, _ = _make_async_chat_stream_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        await agent.chat_stream(buffer_size=512)

        call_tracker.assert_called_once_with(
            channel="C111",
            thread_ts="1234567890.123456",
            recipient_team_id="T111",
            recipient_user_id="W222",
            buffer_size=512,
        )

    @pytest.mark.asyncio
    async def test_import_from_agent_module(self):
        from slack_bolt.agent.async_agent import AsyncBoltAgent as ImportedAsyncBoltAgent

        assert ImportedAsyncBoltAgent is AsyncBoltAgent
