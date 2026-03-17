from unittest.mock import MagicMock

import pytest
from slack_sdk import WebClient

from slack_bolt.context.say_stream.say_stream import SayStream
from slack_bolt.warning import ExperimentalWarning


class TestSayStream:
    def setup_method(self):
        self.mock_client = MagicMock(spec=WebClient)
        self.mock_client.chat_stream = MagicMock()

    def test_missing_channel_raises(self):
        say_stream = SayStream(client=self.mock_client, channel_id=None, thread_ts="111.222")
        with pytest.warns(ExperimentalWarning):
            with pytest.raises(ValueError, match="channel"):
                say_stream()

    def test_missing_thread_ts_raises(self):
        say_stream = SayStream(client=self.mock_client, channel_id="C111", thread_ts=None)
        with pytest.warns(ExperimentalWarning):
            with pytest.raises(ValueError, match="thread_ts"):
                say_stream()

    def test_default_params(self):
        say_stream = SayStream(
            client=self.mock_client,
            channel_id="C111",
            thread_ts="111.222",
            team_id="T111",
            user_id="U111",
        )
        say_stream()

        self.mock_client.chat_stream.assert_called_once_with(
            channel="C111",
            thread_ts="111.222",
            recipient_team_id="T111",
            recipient_user_id="U111",
        )

    def test_parameter_overrides(self):
        say_stream = SayStream(
            client=self.mock_client,
            channel_id="C111",
            thread_ts="111.222",
            team_id="T111",
            user_id="U111",
        )
        say_stream(channel="C222", thread_ts="333.444", recipient_team_id="T222", recipient_user_id="U222")

        self.mock_client.chat_stream.assert_called_once_with(
            channel="C222",
            thread_ts="333.444",
            recipient_team_id="T222",
            recipient_user_id="U222",
        )

    def test_buffer_size_passthrough(self):
        say_stream = SayStream(
            client=self.mock_client,
            channel_id="C111",
            thread_ts="111.222",
        )
        say_stream(buffer_size=100)

        self.mock_client.chat_stream.assert_called_once_with(
            buffer_size=100,
            channel="C111",
            thread_ts="111.222",
            recipient_team_id=None,
            recipient_user_id=None,
        )

    def test_experimental_warning(self):
        say_stream = SayStream(
            client=self.mock_client,
            channel_id="C111",
            thread_ts="111.222",
        )
        with pytest.warns(ExperimentalWarning, match="say_stream is experimental"):
            say_stream()
