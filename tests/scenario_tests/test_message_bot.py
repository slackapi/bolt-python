import json
import re
import time

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt.app import App
from slack_bolt.request import BoltRequest
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestBotMessage:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = WebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body,
            timestamp=timestamp,
        )

    def build_headers(self, timestamp: str, body: str):
        return {
            "content-type": ["application/json"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def build_request(self, event_payload: dict) -> BoltRequest:
        timestamp, body = str(int(time.time())), json.dumps(event_payload)
        return BoltRequest(body=body, headers=self.build_headers(timestamp, body))

    def test_message_handler(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        result = {"call_count": 0}

        @app.message("Hi there!")
        def handle_messages(event, logger):
            logger.info(event)
            result["call_count"] = result["call_count"] + 1

        request = self.build_request(user_message_event_payload)
        response = app.dispatch(request)
        assert response.status == 200

        request = self.build_request(bot_message_event_payload)
        response = app.dispatch(request)
        assert response.status == 200

        request = self.build_request(classic_bot_message_event_payload)
        response = app.dispatch(request)
        assert response.status == 200

        assert_auth_test_count(self, 1)
        time.sleep(1)  # wait a bit after auto ack()
        assert result["call_count"] == 3


user_message_event_payload = {
    "token": "verification-token",
    "team_id": "T111",
    "enterprise_id": "E111",
    "api_app_id": "A111",
    "event": {
        "client_msg_id": "968c94da-c271-4f2a-8ec9-12a9985e5df4",
        "type": "message",
        "text": "Hi there! Thanks for sharing the info!",
        "user": "W111",
        "ts": "1610261659.001400",
        "team": "T111",
        "blocks": [
            {
                "type": "rich_text",
                "block_id": "bN8",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": "Hi there! Thanks for sharing the info!",
                            }
                        ],
                    }
                ],
            }
        ],
        "channel": "C111",
        "event_ts": "1610261659.001400",
        "channel_type": "channel",
    },
    "type": "event_callback",
    "event_id": "Ev111",
    "event_time": 1610261659,
    "authorizations": [
        {
            "enterprise_id": "E111",
            "team_id": "T111",
            "user_id": "W111",
            "is_bot": True,
            "is_enterprise_install": False,
        }
    ],
    "is_ext_shared_channel": False,
    "event_context": "1-message-T111-C111",
}

bot_message_event_payload = {
    "token": "verification-token",
    "team_id": "T111",
    "enterprise_id": "E111",
    "api_app_id": "A111",
    "event": {
        "bot_id": "B999",
        "type": "message",
        "text": "Hi there! Thanks for sharing the info!",
        "user": "UB111",
        "ts": "1610261539.000900",
        "team": "T111",
        "bot_profile": {
            "id": "B999",
            "deleted": False,
            "name": "other-app",
            "updated": 1607307935,
            "app_id": "A222",
            "icons": {
                "image_36": "https://a.slack-edge.com/80588/img/plugins/app/bot_36.png",
                "image_48": "https://a.slack-edge.com/80588/img/plugins/app/bot_48.png",
                "image_72": "https://a.slack-edge.com/80588/img/plugins/app/service_72.png",
            },
            "team_id": "T111",
        },
        "channel": "C111",
        "event_ts": "1610261539.000900",
        "channel_type": "channel",
    },
    "type": "event_callback",
    "event_id": "Ev222",
    "event_time": 1610261539,
    "authorizations": [
        {
            "enterprise_id": "E111",
            "team_id": "T111",
            "user_id": "UB111",
            "is_bot": True,
            "is_enterprise_install": False,
        }
    ],
    "is_ext_shared_channel": False,
    "event_context": "1-message-T111-C111",
}

classic_bot_message_event_payload = {
    "token": "verification-token",
    "team_id": "T111",
    "enterprise_id": "E111",
    "api_app_id": "A111",
    "event": {
        "type": "message",
        "subtype": "bot_message",
        "text": "Hi there! Thanks for sharing the info!",
        "ts": "1610262363.001600",
        "username": "classic-bot",
        "bot_id": "B888",
        "channel": "C111",
        "event_ts": "1610262363.001600",
        "channel_type": "channel",
    },
    "type": "event_callback",
    "event_id": "Ev333",
    "event_time": 1610262363,
    "authorizations": [
        {
            "enterprise_id": "E111",
            "team_id": "T111",
            "user_id": "UB222",
            "is_bot": True,
            "is_enterprise_install": False,
        }
    ],
    "is_ext_shared_channel": False,
    "event_context": "1-message-T111-C111",
}
