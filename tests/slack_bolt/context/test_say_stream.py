import pytest
from slack_sdk import WebClient

from slack_bolt.context.say_stream.say_stream import SayStream
from slack_bolt.warning import ExperimentalWarning
from tests.mock_web_api_server import cleanup_mock_web_api_server, setup_mock_web_api_server


class TestSayStream:
    default_chat_stream_buffer_size = WebClient.chat_stream.__kwdefaults__["buffer_size"]

    def setup_method(self):
        setup_mock_web_api_server(self)
        valid_token = "xoxb-valid"
        mock_api_server_base_url = "http://localhost:8888"
        self.web_client = WebClient(token=valid_token, base_url=mock_api_server_base_url)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)

    def test_missing_channel_raises(self):
        say_stream = SayStream(client=self.web_client, channel=None, thread_ts="111.222")
        with pytest.warns(ExperimentalWarning):
            with pytest.raises(ValueError, match="channel"):
                say_stream()

    def test_missing_thread_ts_raises(self):
        say_stream = SayStream(client=self.web_client, channel="C111", thread_ts=None)
        with pytest.warns(ExperimentalWarning):
            with pytest.raises(ValueError, match="thread_ts"):
                say_stream()

    def test_default_params(self):
        say_stream = SayStream(
            client=self.web_client,
            channel="C111",
            thread_ts="111.222",
            recipient_team_id="T111",
            recipient_user_id="U111",
        )
        stream = say_stream()

        assert stream._buffer_size == self.default_chat_stream_buffer_size
        assert stream._stream_args == {
            "channel": "C111",
            "thread_ts": "111.222",
            "recipient_team_id": "T111",
            "recipient_user_id": "U111",
            "task_display_mode": None,
        }

    def test_parameter_overrides(self):
        say_stream = SayStream(
            client=self.web_client,
            channel="C111",
            thread_ts="111.222",
            recipient_team_id="T111",
            recipient_user_id="U111",
        )
        stream = say_stream(channel="C222", thread_ts="333.444", recipient_team_id="T222", recipient_user_id="U222")

        assert stream._buffer_size == self.default_chat_stream_buffer_size
        assert stream._stream_args == {
            "channel": "C222",
            "thread_ts": "333.444",
            "recipient_team_id": "T222",
            "recipient_user_id": "U222",
            "task_display_mode": None,
        }

    def test_buffer_size_overrides(self):
        say_stream = SayStream(
            client=self.web_client,
            channel="C111",
            thread_ts="111.222",
            recipient_team_id="T111",
            recipient_user_id="U111",
        )
        stream = say_stream(
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

    def test_experimental_warning(self):
        say_stream = SayStream(
            client=self.web_client,
            channel="C111",
            thread_ts="111.222",
        )
        with pytest.warns(ExperimentalWarning, match="say_stream is experimental"):
            say_stream()
