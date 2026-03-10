from unittest.mock import MagicMock

import pytest
from slack_sdk.web import WebClient
from slack_sdk.web.chat_stream import ChatStream

from slack_bolt.context.say_stream.say_stream import SayStream


# TODO: VALIDATE THIS AI SLOP IS CORRECT
class TestSayStream:
    def test_uses_context_defaults(self):
        client = MagicMock(spec=WebClient)
        client.chat_stream.return_value = MagicMock(spec=ChatStream)

        say_stream = SayStream(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        stream = say_stream()

        client.chat_stream.assert_called_once_with(
            channel="C111",
            thread_ts="1234567890.123456",
            recipient_team_id="T111",
            recipient_user_id="W222",
        )
        assert stream is not None

    def test_overrides_context_defaults(self):
        client = MagicMock(spec=WebClient)
        client.chat_stream.return_value = MagicMock(spec=ChatStream)

        say_stream = SayStream(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        stream = say_stream(
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

    def test_rejects_partial_overrides(self):
        client = MagicMock(spec=WebClient)
        say_stream = SayStream(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        with pytest.raises(ValueError, match="Either provide all of"):
            say_stream(channel="C999")

    def test_passes_extra_kwargs(self):
        client = MagicMock(spec=WebClient)
        client.chat_stream.return_value = MagicMock(spec=ChatStream)

        say_stream = SayStream(
            client=client,
            channel_id="C111",
            thread_ts="1234567890.123456",
            team_id="T111",
            user_id="W222",
        )
        say_stream(buffer_size=512)

        client.chat_stream.assert_called_once_with(
            channel="C111",
            thread_ts="1234567890.123456",
            recipient_team_id="T111",
            recipient_user_id="W222",
            buffer_size=512,
        )

    def test_raises_without_channel_id(self):
        client = MagicMock(spec=WebClient)
        say_stream = SayStream(client=client, channel_id=None, thread_ts="1234567890.123456")
        with pytest.raises(ValueError, match="no channel_id"):
            say_stream()

    def test_raises_without_thread_ts(self):
        client = MagicMock(spec=WebClient)
        say_stream = SayStream(client=client, channel_id="C111", thread_ts=None)
        with pytest.raises(ValueError, match="no thread_ts"):
            say_stream()

    def test_import_from_slack_bolt(self):
        from slack_bolt import SayStream as ImportedSayStream

        assert ImportedSayStream is SayStream
