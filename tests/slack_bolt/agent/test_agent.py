from unittest.mock import MagicMock

import pytest
from slack_sdk.web import WebClient
from slack_sdk.web.chat_stream import ChatStream

from slack_bolt.agent.agent import BoltAgent


class TestBoltAgent:
    def test_chat_stream_uses_context_defaults(self):
        """BoltAgent.chat_stream() passes context defaults to WebClient.chat_stream()."""
        client = MagicMock(spec=WebClient)
        client.chat_stream.return_value = MagicMock(spec=ChatStream)

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        stream = agent.chat_stream()

        client.chat_stream.assert_called_once_with(
            channel="C111",
            thread_ts="1234567890.123456",
            recipient_team_id="T111",
            recipient_user_id="W222",
        )
        assert stream is not None

    def test_chat_stream_overrides_context_defaults(self):
        """Explicit kwargs to chat_stream() override context defaults."""
        client = MagicMock(spec=WebClient)
        client.chat_stream.return_value = MagicMock(spec=ChatStream)

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        stream = agent.chat_stream(
            channel="C999",
            thread_ts="9999999999.999999",
            recipient_team_id="T999",
            recipient_user_id="U999",
        )

        client.chat_stream.assert_called_once_with(
            channel="C999",
            thread_ts="9999999999.999999",
            recipient_team_id="T999",
            recipient_user_id="U999",
        )
        assert stream is not None

    def test_chat_stream_rejects_partial_overrides(self):
        """Passing only some of the four context args raises ValueError."""
        client = MagicMock(spec=WebClient)
        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        with pytest.raises(ValueError, match="Either provide all of"):
            agent.chat_stream(channel="C999")

    def test_chat_stream_passes_extra_kwargs(self):
        """Extra kwargs are forwarded to WebClient.chat_stream()."""
        client = MagicMock(spec=WebClient)
        client.chat_stream.return_value = MagicMock(spec=ChatStream)

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        agent.chat_stream(buffer_size=512)

        client.chat_stream.assert_called_once_with(
            channel="C111",
            thread_ts="1234567890.123456",
            recipient_team_id="T111",
            recipient_user_id="W222",
            buffer_size=512,
        )

    def test_chat_stream_falls_back_to_ts(self):
        """When thread_ts is not set, chat_stream() falls back to ts."""
        client = MagicMock(spec=WebClient)
        client.chat_stream.return_value = MagicMock(spec=ChatStream)

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            team_id="T111",
            ts="1111111111.111111",
            user_id="W222",
        )
        stream = agent.chat_stream()

        client.chat_stream.assert_called_once_with(
            channel="C111",
            thread_ts="1111111111.111111",
            recipient_team_id="T111",
            recipient_user_id="W222",
        )
        assert stream is not None

    def test_chat_stream_prefers_thread_ts_over_ts(self):
        """thread_ts takes priority over ts."""
        client = MagicMock(spec=WebClient)
        client.chat_stream.return_value = MagicMock(spec=ChatStream)

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            team_id="T111",
            thread_ts="1234567890.123456",
            ts="1111111111.111111",
            user_id="W222",
        )
        stream = agent.chat_stream()

        client.chat_stream.assert_called_once_with(
            channel="C111",
            thread_ts="1234567890.123456",
            recipient_team_id="T111",
            recipient_user_id="W222",
        )
        assert stream is not None

    def test_set_status_uses_context_defaults(self):
        """BoltAgent.set_status() passes context defaults to WebClient.assistant_threads_setStatus()."""
        client = MagicMock(spec=WebClient)
        client.assistant_threads_setStatus.return_value = MagicMock()

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        agent.set_status(status="Thinking...")

        client.assistant_threads_setStatus.assert_called_once_with(
            channel_id="C111",
            thread_ts="1234567890.123456",
            status="Thinking...",
            loading_messages=None,
        )

    def test_set_status_with_loading_messages(self):
        """BoltAgent.set_status() forwards loading_messages."""
        client = MagicMock(spec=WebClient)
        client.assistant_threads_setStatus.return_value = MagicMock()

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        agent.set_status(
            status="Thinking...",
            loading_messages=["Sitting...", "Waiting..."],
        )

        client.assistant_threads_setStatus.assert_called_once_with(
            channel_id="C111",
            thread_ts="1234567890.123456",
            status="Thinking...",
            loading_messages=["Sitting...", "Waiting..."],
        )

    def test_set_status_overrides_context_defaults(self):
        """Explicit channel_id/thread_ts override context defaults."""
        client = MagicMock(spec=WebClient)
        client.assistant_threads_setStatus.return_value = MagicMock()

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        agent.set_status(
            status="Thinking...",
            channel_id="C999",
            thread_ts="9999999999.999999",
        )

        client.assistant_threads_setStatus.assert_called_once_with(
            channel_id="C999",
            thread_ts="9999999999.999999",
            status="Thinking...",
            loading_messages=None,
        )

    def test_set_status_passes_extra_kwargs(self):
        """Extra kwargs are forwarded to WebClient.assistant_threads_setStatus()."""
        client = MagicMock(spec=WebClient)
        client.assistant_threads_setStatus.return_value = MagicMock()

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        agent.set_status(status="Thinking...", token="xoxb-override")

        client.assistant_threads_setStatus.assert_called_once_with(
            channel_id="C111",
            thread_ts="1234567890.123456",
            status="Thinking...",
            loading_messages=None,
            token="xoxb-override",
        )

    def test_set_status_requires_status(self):
        """set_status() raises TypeError when status is not provided."""
        client = MagicMock(spec=WebClient)
        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        with pytest.raises(TypeError):
            agent.set_status()

    def test_set_suggested_prompts_uses_context_defaults(self):
        """BoltAgent.set_suggested_prompts() passes context defaults to WebClient.assistant_threads_setSuggestedPrompts()."""
        client = MagicMock(spec=WebClient)
        client.assistant_threads_setSuggestedPrompts.return_value = MagicMock()

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        agent.set_suggested_prompts(prompts=["What can you do?", "Help me write code"])

        client.assistant_threads_setSuggestedPrompts.assert_called_once_with(
            channel_id="C111",
            thread_ts="1234567890.123456",
            prompts=[
                {"title": "What can you do?", "message": "What can you do?"},
                {"title": "Help me write code", "message": "Help me write code"},
            ],
            title=None,
        )

    def test_set_suggested_prompts_with_dict_prompts(self):
        """BoltAgent.set_suggested_prompts() accepts dict prompts with title and message."""
        client = MagicMock(spec=WebClient)
        client.assistant_threads_setSuggestedPrompts.return_value = MagicMock()

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        agent.set_suggested_prompts(
            prompts=[
                {"title": "Short title", "message": "A much longer message for this prompt"},
            ],
            title="Suggestions",
        )

        client.assistant_threads_setSuggestedPrompts.assert_called_once_with(
            channel_id="C111",
            thread_ts="1234567890.123456",
            prompts=[
                {"title": "Short title", "message": "A much longer message for this prompt"},
            ],
            title="Suggestions",
        )

    def test_set_suggested_prompts_overrides_context_defaults(self):
        """Explicit channel_id/thread_ts override context defaults."""
        client = MagicMock(spec=WebClient)
        client.assistant_threads_setSuggestedPrompts.return_value = MagicMock()

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        agent.set_suggested_prompts(
            prompts=["Hello"],
            channel_id="C999",
            thread_ts="9999999999.999999",
        )

        client.assistant_threads_setSuggestedPrompts.assert_called_once_with(
            channel_id="C999",
            thread_ts="9999999999.999999",
            prompts=[{"title": "Hello", "message": "Hello"}],
            title=None,
        )

    def test_set_suggested_prompts_passes_extra_kwargs(self):
        """Extra kwargs are forwarded to WebClient.assistant_threads_setSuggestedPrompts()."""
        client = MagicMock(spec=WebClient)
        client.assistant_threads_setSuggestedPrompts.return_value = MagicMock()

        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        agent.set_suggested_prompts(prompts=["Hello"], token="xoxb-override")

        client.assistant_threads_setSuggestedPrompts.assert_called_once_with(
            channel_id="C111",
            thread_ts="1234567890.123456",
            prompts=[{"title": "Hello", "message": "Hello"}],
            title=None,
            token="xoxb-override",
        )

    def test_set_suggested_prompts_requires_prompts(self):
        """set_suggested_prompts() raises TypeError when prompts is not provided."""
        client = MagicMock(spec=WebClient)
        agent = BoltAgent(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        with pytest.raises(TypeError):
            agent.set_suggested_prompts()

    def test_import_from_slack_bolt(self):
        from slack_bolt import BoltAgent as ImportedBoltAgent

        assert ImportedBoltAgent is BoltAgent

    def test_import_from_agent_module(self):
        from slack_bolt.agent import BoltAgent as ImportedBoltAgent

        assert ImportedBoltAgent is BoltAgent
