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


def _make_async_api_mock():
    mock_response = MagicMock()
    call_tracker = MagicMock()

    async def fake_api_call(**kwargs):
        call_tracker(**kwargs)
        return mock_response

    return fake_api_call, call_tracker, mock_response


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
    async def test_chat_stream_falls_back_to_ts(self):
        """When thread_ts is not set, chat_stream() falls back to ts."""
        client = MagicMock(spec=AsyncWebClient)
        client.chat_stream, call_tracker, _ = _make_async_chat_stream_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            team_id="T111",
            ts="1111111111.111111",
            user_id="W222",
        )
        stream = await agent.chat_stream()

        call_tracker.assert_called_once_with(
            channel="C111",
            thread_ts="1111111111.111111",
            recipient_team_id="T111",
            recipient_user_id="W222",
        )
        assert stream is not None

    @pytest.mark.asyncio
    async def test_chat_stream_prefers_thread_ts_over_ts(self):
        """thread_ts takes priority over ts."""
        client = MagicMock(spec=AsyncWebClient)
        client.chat_stream, call_tracker, _ = _make_async_chat_stream_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            team_id="T111",
            thread_ts="1234567890.123456",
            ts="1111111111.111111",
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
    async def test_set_status_uses_context_defaults(self):
        """AsyncBoltAgent.set_status() passes context defaults to AsyncWebClient.assistant_threads_setStatus()."""
        client = MagicMock(spec=AsyncWebClient)
        client.assistant_threads_setStatus, call_tracker, _ = _make_async_api_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        await agent.set_status(status="Thinking...")

        call_tracker.assert_called_once_with(
            channel_id="C111",
            thread_ts="1234567890.123456",
            status="Thinking...",
            loading_messages=None,
        )

    @pytest.mark.asyncio
    async def test_set_status_with_loading_messages(self):
        """AsyncBoltAgent.set_status() forwards loading_messages."""
        client = MagicMock(spec=AsyncWebClient)
        client.assistant_threads_setStatus, call_tracker, _ = _make_async_api_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        await agent.set_status(
            status="Thinking...",
            loading_messages=["Sitting...", "Waiting..."],
        )

        call_tracker.assert_called_once_with(
            channel_id="C111",
            thread_ts="1234567890.123456",
            status="Thinking...",
            loading_messages=["Sitting...", "Waiting..."],
        )

    @pytest.mark.asyncio
    async def test_set_status_overrides_context_defaults(self):
        """Explicit channel_id/thread_ts override context defaults."""
        client = MagicMock(spec=AsyncWebClient)
        client.assistant_threads_setStatus, call_tracker, _ = _make_async_api_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        await agent.set_status(
            status="Thinking...",
            channel_id="C999",
            thread_ts="9999999999.999999",
        )

        call_tracker.assert_called_once_with(
            channel_id="C999",
            thread_ts="9999999999.999999",
            status="Thinking...",
            loading_messages=None,
        )

    @pytest.mark.asyncio
    async def test_set_status_passes_extra_kwargs(self):
        """Extra kwargs are forwarded to AsyncWebClient.assistant_threads_setStatus()."""
        client = MagicMock(spec=AsyncWebClient)
        client.assistant_threads_setStatus, call_tracker, _ = _make_async_api_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        await agent.set_status(status="Thinking...", token="xoxb-override")

        call_tracker.assert_called_once_with(
            channel_id="C111",
            thread_ts="1234567890.123456",
            status="Thinking...",
            loading_messages=None,
            token="xoxb-override",
        )

    @pytest.mark.asyncio
    async def test_set_status_requires_status(self):
        """set_status() raises TypeError when status is not provided."""
        client = MagicMock(spec=AsyncWebClient)
        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        with pytest.raises(TypeError):
            await agent.set_status()

    @pytest.mark.asyncio
    async def test_set_suggested_prompts_uses_context_defaults(self):
        """AsyncBoltAgent.set_suggested_prompts() passes context defaults to AsyncWebClient.assistant_threads_setSuggestedPrompts()."""
        client = MagicMock(spec=AsyncWebClient)
        client.assistant_threads_setSuggestedPrompts, call_tracker, _ = _make_async_api_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        await agent.set_suggested_prompts(prompts=["What can you do?", "Help me write code"])

        call_tracker.assert_called_once_with(
            channel_id="C111",
            thread_ts="1234567890.123456",
            prompts=[
                {"title": "What can you do?", "message": "What can you do?"},
                {"title": "Help me write code", "message": "Help me write code"},
            ],
            title=None,
        )

    @pytest.mark.asyncio
    async def test_set_suggested_prompts_with_dict_prompts(self):
        """AsyncBoltAgent.set_suggested_prompts() accepts dict prompts with title and message."""
        client = MagicMock(spec=AsyncWebClient)
        client.assistant_threads_setSuggestedPrompts, call_tracker, _ = _make_async_api_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        await agent.set_suggested_prompts(
            prompts=[
                {"title": "Short title", "message": "A much longer message for this prompt"},
            ],
            title="Suggestions",
        )

        call_tracker.assert_called_once_with(
            channel_id="C111",
            thread_ts="1234567890.123456",
            prompts=[
                {"title": "Short title", "message": "A much longer message for this prompt"},
            ],
            title="Suggestions",
        )

    @pytest.mark.asyncio
    async def test_set_suggested_prompts_overrides_context_defaults(self):
        """Explicit channel_id/thread_ts override context defaults."""
        client = MagicMock(spec=AsyncWebClient)
        client.assistant_threads_setSuggestedPrompts, call_tracker, _ = _make_async_api_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        await agent.set_suggested_prompts(
            prompts=["Hello"],
            channel_id="C999",
            thread_ts="9999999999.999999",
        )

        call_tracker.assert_called_once_with(
            channel_id="C999",
            thread_ts="9999999999.999999",
            prompts=[{"title": "Hello", "message": "Hello"}],
            title=None,
        )

    @pytest.mark.asyncio
    async def test_set_suggested_prompts_passes_extra_kwargs(self):
        """Extra kwargs are forwarded to AsyncWebClient.assistant_threads_setSuggestedPrompts()."""
        client = MagicMock(spec=AsyncWebClient)
        client.assistant_threads_setSuggestedPrompts, call_tracker, _ = _make_async_api_mock()

        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        await agent.set_suggested_prompts(prompts=["Hello"], token="xoxb-override")

        call_tracker.assert_called_once_with(
            channel_id="C111",
            thread_ts="1234567890.123456",
            prompts=[{"title": "Hello", "message": "Hello"}],
            title=None,
            token="xoxb-override",
        )

    @pytest.mark.asyncio
    async def test_set_suggested_prompts_requires_prompts(self):
        """set_suggested_prompts() raises TypeError when prompts is not provided."""
        client = MagicMock(spec=AsyncWebClient)
        agent = AsyncBoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        with pytest.raises(TypeError):
            await agent.set_suggested_prompts()

    @pytest.mark.asyncio
    async def test_import_from_agent_module(self):
        from slack_bolt.agent.async_agent import AsyncBoltAgent as ImportedAsyncBoltAgent

        assert ImportedAsyncBoltAgent is AsyncBoltAgent
