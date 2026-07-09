from slack_bolt.request.payload_utils import (
    is_event,
    is_message_event,
    is_any_im_message_event,
    is_im_message_event,
    is_assistant_event,
    is_assistant_thread_started_event,
    is_assistant_thread_context_changed_event,
    is_app_home_opened_event,
    is_user_message_event_in_assistant_thread,
    is_bot_message_event_in_assistant_thread,
    is_other_message_sub_event_in_assistant_thread,
)
from tests.scenario_tests.test_events_assistant import (
    build_payload,
    thread_started_event_body,
    thread_context_changed_event_body,
    user_message_event_body,
    user_message_event_body_with_assistant_thread,
    message_changed_event_body,
    channel_user_message_event_body,
    channel_message_changed_event_body,
)
from tests.scenario_tests.test_message_bot import (
    bot_message_event_payload,
    classic_bot_message_event_payload,
)
from tests.scenario_tests.test_message_deleted import event_payload as message_deleted_channel_body
from tests.scenario_tests.test_events_ignore_self import event_body as reaction_added_event_body
from tests.scenario_tests.test_block_actions import body as block_actions_body

file_share_im_message_body = build_payload(
    {
        "user": "W222",
        "type": "message",
        "subtype": "file_share",
        "ts": "1726133700.887259",
        "text": "uploaded a file",
        "files": [
            {
                "id": "F111",
                "created": 1726133700,
                "name": "test.png",
                "title": "test.png",
                "mimetype": "image/png",
                "filetype": "png",
                "user": "W222",
                "size": 12345,
                "mode": "hosted",
                "is_external": False,
                "is_public": False,
                "url_private": "https://files.slack.com/files-pri/T111-F111/test.png",
                "permalink": "https://example.slack.com/files/W222/F111/test.png",
            }
        ],
        "upload": True,
        "display_as_bot": False,
        "thread_ts": "1726133698.626339",
        "channel": "D111",
        "event_ts": "1726133700.887259",
        "channel_type": "im",
    }
)

bot_im_thread_message_body = build_payload(
    {
        "type": "message",
        "ts": "1726133700.887259",
        "text": "Here is your answer",
        "user": "UB111",
        "bot_id": "B111",
        "app_id": "A222",
        "bot_profile": {
            "id": "B111",
            "deleted": False,
            "name": "assistant-app",
            "updated": 1726133600,
            "app_id": "A222",
            "team_id": "T111",
        },
        "thread_ts": "1726133698.626339",
        "channel": "D111",
        "event_ts": "1726133700.887259",
        "channel_type": "im",
    }
)

im_message_no_thread_ts_body = build_payload(
    {
        "user": "W222",
        "type": "message",
        "ts": "1726133700.887259",
        "text": "A top-level DM, not in a thread",
        "channel": "D111",
        "event_ts": "1726133700.887259",
        "channel_type": "im",
    }
)

app_home_opened_messages_body = build_payload(
    {
        "type": "app_home_opened",
        "user": "W222",
        "channel": "D111",
        "tab": "messages",
        "event_ts": "1726133700.887259",
    }
)

app_home_opened_home_body = build_payload(
    {
        "type": "app_home_opened",
        "user": "W222",
        "channel": "D111",
        "tab": "home",
        "event_ts": "1726133700.887259",
    }
)

slash_command_body = {
    "token": "verification_token",
    "command": "/test",
    "text": "hello",
    "user_id": "U111",
    "user_name": "primary-owner",
    "channel_id": "C111",
    "channel_name": "test-channel",
    "team_id": "T111",
    "team_domain": "test-domain",
    "api_app_id": "A111",
    "is_enterprise_install": "false",
    "response_url": "https://hooks.slack.com/commands/T111/111/xxx",
    "trigger_id": "111.222.xxx",
}


class TestPayloadUtils:
    def test_is_message_event(self):
        positives = {
            "user_message_im": user_message_event_body,
            "user_message_im_with_assistant_thread": user_message_event_body_with_assistant_thread,
            "message_changed_im": message_changed_event_body,
            "channel_user_message": channel_user_message_event_body,
            "channel_message_changed": channel_message_changed_event_body,
            "bot_message_channel": bot_message_event_payload,
            "classic_bot_message_channel": classic_bot_message_event_payload,
            "message_deleted_channel": message_deleted_channel_body,
            "file_share_im": file_share_im_message_body,
            "bot_im_thread": bot_im_thread_message_body,
            "im_no_thread_ts": im_message_no_thread_ts_body,
        }
        negatives = {
            "thread_started": thread_started_event_body,
            "thread_context_changed": thread_context_changed_event_body,
            "reaction_added": reaction_added_event_body,
            "block_actions": block_actions_body,
            "slash_command": slash_command_body,
            "empty_dict": {},
        }
        for key, body in positives.items():
            assert is_message_event(body), f"{key} should be recognized as a message event"
        for key, body in negatives.items():
            assert not is_message_event(body), f"{key} should NOT be recognized as a message event"

    def test_is_any_im_message_event(self):
        positives = {
            "user_message_im": user_message_event_body,
            "user_message_im_with_assistant_thread": user_message_event_body_with_assistant_thread,
            "message_changed_im": message_changed_event_body,
            "file_share_im": file_share_im_message_body,
            "bot_im_thread": bot_im_thread_message_body,
            "im_no_thread_ts": im_message_no_thread_ts_body,
        }
        negatives = {
            "channel_user_message": channel_user_message_event_body,
            "channel_message_changed": channel_message_changed_event_body,
            "bot_message_channel": bot_message_event_payload,
            "classic_bot_message_channel": classic_bot_message_event_payload,
            "message_deleted_channel": message_deleted_channel_body,
            "thread_started": thread_started_event_body,
            "thread_context_changed": thread_context_changed_event_body,
            "reaction_added": reaction_added_event_body,
            "block_actions": block_actions_body,
            "slash_command": slash_command_body,
        }
        for key, body in positives.items():
            assert is_any_im_message_event(body), f"{key} should pass {is_any_im_message_event.__name__}"
        for key, body in negatives.items():
            assert not is_any_im_message_event(body), f"{key} should NOT pass {is_any_im_message_event.__name__}"

    def test_is_im_message_event(self):
        # subtype must be None or "file_share" to pass
        positives = {
            "user_message_im": user_message_event_body,
            "user_message_im_with_assistant_thread": user_message_event_body_with_assistant_thread,
            "file_share_im": file_share_im_message_body,
            "bot_im_thread": bot_im_thread_message_body,
            "im_no_thread_ts": im_message_no_thread_ts_body,
        }
        negatives = {
            "message_changed_im": message_changed_event_body,
            "channel_user_message": channel_user_message_event_body,
            "channel_message_changed": channel_message_changed_event_body,
            "classic_bot_message_channel": classic_bot_message_event_payload,
            "bot_message_channel": bot_message_event_payload,
            "message_deleted_channel": message_deleted_channel_body,
            "thread_started": thread_started_event_body,
            "thread_context_changed": thread_context_changed_event_body,
            "reaction_added": reaction_added_event_body,
            "block_actions": block_actions_body,
        }
        for key, body in positives.items():
            assert is_im_message_event(body), f"{key} should pass {is_im_message_event.__name__}"
        for key, body in negatives.items():
            assert not is_im_message_event(body), f"{key} should NOT pass {is_im_message_event.__name__}"

    def test_is_event(self):
        positives = {
            "thread_started": thread_started_event_body,
            "thread_context_changed": thread_context_changed_event_body,
            "user_message_im": user_message_event_body,
            "user_message_im_with_assistant_thread": user_message_event_body_with_assistant_thread,
            "message_changed_im": message_changed_event_body,
            "channel_user_message": channel_user_message_event_body,
            "channel_message_changed": channel_message_changed_event_body,
            "bot_message_channel": bot_message_event_payload,
            "classic_bot_message_channel": classic_bot_message_event_payload,
            "message_deleted_channel": message_deleted_channel_body,
            "reaction_added": reaction_added_event_body,
            "file_share_im": file_share_im_message_body,
            "bot_im_thread": bot_im_thread_message_body,
            "im_no_thread_ts": im_message_no_thread_ts_body,
        }
        negatives = {
            "block_actions": block_actions_body,
            "slash_command": slash_command_body,
            "empty_dict": {},
        }
        for key, body in positives.items():
            assert is_event(body), f"{key} should be recognized as an event"
        for key, body in negatives.items():
            assert not is_event(body), f"{key} should NOT be recognized as an event"

    def test_is_user_message_event_in_assistant_thread(self):
        # Requires: is_im_message_event + thread_ts present + bot_id absent
        positives = {
            "user_message_im": user_message_event_body,
            "user_message_im_with_assistant_thread": user_message_event_body_with_assistant_thread,
            "file_share_im": file_share_im_message_body,
        }
        negatives = {
            "bot_im_thread": bot_im_thread_message_body,
            "im_no_thread_ts": im_message_no_thread_ts_body,
            "message_changed_im": message_changed_event_body,
            "channel_user_message": channel_user_message_event_body,
            "channel_message_changed": channel_message_changed_event_body,
            "bot_message_channel": bot_message_event_payload,
            "thread_started": thread_started_event_body,
            "thread_context_changed": thread_context_changed_event_body,
            "reaction_added": reaction_added_event_body,
            "block_actions": block_actions_body,
        }
        for key, body in positives.items():
            assert is_user_message_event_in_assistant_thread(
                body
            ), f"{key} should pass {is_user_message_event_in_assistant_thread.__name__}"
        for key, body in negatives.items():
            assert not is_user_message_event_in_assistant_thread(
                body
            ), f"{key} should NOT pass {is_user_message_event_in_assistant_thread.__name__}"

    def test_is_bot_message_event_in_assistant_thread(self):
        positives = {
            "bot_im_thread": bot_im_thread_message_body,
        }
        negatives = {
            "user_message_im": user_message_event_body,
            "file_share_im": file_share_im_message_body,
            "im_no_thread_ts": im_message_no_thread_ts_body,
            "message_changed_im": message_changed_event_body,
            "channel_user_message": channel_user_message_event_body,
            "bot_message_channel": bot_message_event_payload,
            "classic_bot_message_channel": classic_bot_message_event_payload,
            "thread_started": thread_started_event_body,
            "thread_context_changed": thread_context_changed_event_body,
            "reaction_added": reaction_added_event_body,
            "block_actions": block_actions_body,
        }
        for key, body in positives.items():
            assert is_bot_message_event_in_assistant_thread(
                body
            ), f"{key} should pass {is_bot_message_event_in_assistant_thread.__name__}"
        for key, body in negatives.items():
            assert not is_bot_message_event_in_assistant_thread(
                body
            ), f"{key} should NOT pass {is_bot_message_event_in_assistant_thread.__name__}"

    def test_is_bot_message_user_message_asymmetry(self):
        assert is_user_message_event_in_assistant_thread(file_share_im_message_body)
        assert not is_bot_message_event_in_assistant_thread(file_share_im_message_body)

        assert is_bot_message_event_in_assistant_thread(bot_im_thread_message_body)
        assert not is_user_message_event_in_assistant_thread(bot_im_thread_message_body)

    def test_is_other_message_sub_event_in_assistant_thread(self):
        positives = {
            "message_changed_im": message_changed_event_body,
        }
        negatives = {
            "user_message_im": user_message_event_body,
            "bot_im_thread": bot_im_thread_message_body,
            "im_no_thread_ts": im_message_no_thread_ts_body,
            "channel_message_changed": channel_message_changed_event_body,
            "channel_user_message": channel_user_message_event_body,
            "message_deleted_channel": message_deleted_channel_body,
            "thread_started": thread_started_event_body,
            "reaction_added": reaction_added_event_body,
            "block_actions": block_actions_body,
        }
        for key, body in positives.items():
            assert is_other_message_sub_event_in_assistant_thread(
                body
            ), f"{key} should pass {is_other_message_sub_event_in_assistant_thread.__name__}"
        for key, body in negatives.items():
            assert not is_other_message_sub_event_in_assistant_thread(
                body
            ), f"{key} should NOT pass {is_other_message_sub_event_in_assistant_thread.__name__}"

    def test_is_assistant_event(self):
        positives = {
            "thread_started": thread_started_event_body,
            "thread_context_changed": thread_context_changed_event_body,
            "user_message_im": user_message_event_body,
            "user_message_im_with_assistant_thread": user_message_event_body_with_assistant_thread,
            "file_share_im": file_share_im_message_body,
            "bot_im_thread": bot_im_thread_message_body,
        }
        negatives = {
            "message_changed_im": message_changed_event_body,
            "im_no_thread_ts": im_message_no_thread_ts_body,
            "channel_user_message": channel_user_message_event_body,
            "channel_message_changed": channel_message_changed_event_body,
            "bot_message_channel": bot_message_event_payload,
            "classic_bot_message_channel": classic_bot_message_event_payload,
            "message_deleted_channel": message_deleted_channel_body,
            "reaction_added": reaction_added_event_body,
            "block_actions": block_actions_body,
        }
        for key, body in positives.items():
            assert is_assistant_event(body), f"{key} should pass {is_assistant_event.__name__}"
        for key, body in negatives.items():
            assert not is_assistant_event(body), f"{key} should NOT pass {is_assistant_event.__name__}"

    def test_is_assistant_thread_started_event(self):
        assert is_assistant_thread_started_event(thread_started_event_body)

        negatives = {
            "thread_context_changed": thread_context_changed_event_body,
            "user_message_im": user_message_event_body,
            "message_changed_im": message_changed_event_body,
            "bot_im_thread": bot_im_thread_message_body,
            "channel_user_message": channel_user_message_event_body,
            "reaction_added": reaction_added_event_body,
            "block_actions": block_actions_body,
        }
        for key, body in negatives.items():
            assert not is_assistant_thread_started_event(
                body
            ), f"{key} should NOT pass {is_assistant_thread_started_event.__name__}"

    def test_is_assistant_thread_context_changed_event(self):
        assert is_assistant_thread_context_changed_event(thread_context_changed_event_body)

        negatives = {
            "thread_started": thread_started_event_body,
            "user_message_im": user_message_event_body,
            "message_changed_im": message_changed_event_body,
            "bot_im_thread": bot_im_thread_message_body,
            "channel_user_message": channel_user_message_event_body,
            "reaction_added": reaction_added_event_body,
            "block_actions": block_actions_body,
        }
        for key, body in negatives.items():
            assert not is_assistant_thread_context_changed_event(
                body
            ), f"{key} should NOT pass {is_assistant_thread_context_changed_event.__name__}"

    def test_is_app_home_opened_event(self):
        assert is_app_home_opened_event(app_home_opened_messages_body)
        assert is_app_home_opened_event(app_home_opened_home_body)

        assert is_app_home_opened_event(app_home_opened_messages_body, tab="messages")
        assert not is_app_home_opened_event(app_home_opened_home_body, tab="messages")

        negatives = {
            "thread_started": thread_started_event_body,
            "thread_context_changed": thread_context_changed_event_body,
            "user_message_im": user_message_event_body,
            "channel_user_message": channel_user_message_event_body,
            "reaction_added": reaction_added_event_body,
            "block_actions": block_actions_body,
            "empty_dict": {},
        }
        for key, body in negatives.items():
            assert not is_app_home_opened_event(body), f"{key} should NOT pass {is_app_home_opened_event.__name__}"
            assert not is_app_home_opened_event(
                body, tab="messages"
            ), f"{key} should NOT pass {is_app_home_opened_event.__name__} with tab='messages'"
