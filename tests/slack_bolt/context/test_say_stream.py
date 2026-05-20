import pytest
from unittest.mock import patch, MagicMock

from slack_sdk import WebClient

from slack_bolt.context.say_stream.say_stream import SayStream


class TestSayStream:
    def setup_method(self):
        self.web_client = WebClient(token="xoxb-valid")

    def test_missing_channel_raises(self):
        say_stream = SayStream(client=self.web_client, channel=None, thread_ts="111.222")
        with pytest.raises(ValueError, match="channel"):
            say_stream()

    def test_missing_thread_ts_raises(self):
        say_stream = SayStream(client=self.web_client, channel="C111", thread_ts=None)
        with pytest.raises(ValueError, match="thread_ts"):
            say_stream()

    def test_default_params(self):
        say_stream = SayStream(
            client=self.web_client,
            channel="C111",
            recipient_team_id="T111",
            recipient_user_id="U111",
            thread_ts="111.222",
        )
        with patch.object(self.web_client, "chat_stream", return_value=MagicMock()) as mock_chat_stream:
            say_stream()
            mock_chat_stream.assert_called_once_with(
                channel="C111",
                recipient_team_id="T111",
                recipient_user_id="U111",
                thread_ts="111.222",
                icon_emoji=None,
                icon_url=None,
                username=None,
            )

    def test_parameter_overrides(self):
        say_stream = SayStream(
            client=self.web_client,
            channel="C111",
            recipient_team_id="T111",
            recipient_user_id="U111",
            thread_ts="111.222",
        )
        with patch.object(self.web_client, "chat_stream", return_value=MagicMock()) as mock_chat_stream:
            say_stream(channel="C222", thread_ts="333.444", recipient_team_id="T222", recipient_user_id="U222")
            mock_chat_stream.assert_called_once_with(
                channel="C222",
                recipient_team_id="T222",
                recipient_user_id="U222",
                thread_ts="333.444",
                icon_emoji=None,
                icon_url=None,
                username=None,
            )

    def test_buffer_size_overrides(self):
        say_stream = SayStream(
            client=self.web_client,
            channel="C111",
            recipient_team_id="T111",
            recipient_user_id="U111",
            thread_ts="111.222",
        )
        with patch.object(self.web_client, "chat_stream", return_value=MagicMock()) as mock_chat_stream:
            say_stream(
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

    def test_authorship_overrides(self):
        say_stream = SayStream(
            client=self.web_client,
            channel="C111",
            recipient_team_id="T111",
            recipient_user_id="U111",
            thread_ts="111.222",
        )
        with patch.object(self.web_client, "chat_stream", return_value=MagicMock()) as mock_chat_stream:
            say_stream(icon_emoji=":maple_leaf:", username="Charlie Brown")
            mock_chat_stream.assert_called_once_with(
                channel="C111",
                recipient_team_id="T111",
                recipient_user_id="U111",
                thread_ts="111.222",
                icon_emoji=":maple_leaf:",
                icon_url=None,
                username="Charlie Brown",
            )
