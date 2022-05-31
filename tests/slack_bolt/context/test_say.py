import pytest
from slack_sdk import WebClient
from slack_sdk.web import SlackResponse

from slack_bolt import Say
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)


class TestSay:
    def setup_method(self):
        setup_mock_web_api_server(self)
        valid_token = "xoxb-valid"
        mock_api_server_base_url = "http://localhost:8888"
        self.web_client = WebClient(token=valid_token, base_url=mock_api_server_base_url)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)

    def test_say(self):
        say = Say(client=self.web_client, channel="C111")
        response: SlackResponse = say(text="Hi there!")
        assert response.status_code == 200

    def test_say_unfurl_options(self):
        say = Say(client=self.web_client, channel="C111")
        response: SlackResponse = say(text="Hi there!", unfurl_media=True, unfurl_links=True)
        assert response.status_code == 200

    def test_say_dict(self):
        say = Say(client=self.web_client, channel="C111")
        response: SlackResponse = say({"text": "Hi!"})
        assert response.status_code == 200

    def test_say_dict_channel(self):
        say = Say(client=self.web_client, channel="C111")
        response: SlackResponse = say({"text": "Hi!", "channel": "C111"})
        assert response.status_code == 200

    def test_say_invalid(self):
        say = Say(client=self.web_client, channel="C111")
        with pytest.raises(ValueError):
            say([])
