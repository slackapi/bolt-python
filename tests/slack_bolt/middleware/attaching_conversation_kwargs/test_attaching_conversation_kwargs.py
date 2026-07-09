from slack_sdk import WebClient

from slack_bolt.middleware.attaching_conversation_kwargs import AttachingConversationKwargs
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from tests.scenario_tests.test_events_assistant import (
    build_payload,
    thread_started_event_body,
    user_message_event_body,
    channel_user_message_event_body,
)


def next():
    return BoltResponse(status=200)


ASSISTANT_KWARGS = ("say", "set_title", "set_suggested_prompts", "get_thread_context", "save_thread_context")

# A top-level DM (not in a thread) is not an assistant thread, but set_suggested_prompts is still attached.
top_level_im_message_event_body = build_payload(
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

# A bot-authored top-level DM is also in scope: set_suggested_prompts is attached for any IM message.
bot_im_message_event_body = build_payload(
    {
        "type": "message",
        "ts": "1726133700.887259",
        "text": "A DM authored by a bot",
        "user": "UB111",
        "bot_id": "B111",
        "app_id": "A222",
        "channel": "D111",
        "event_ts": "1726133700.887259",
        "channel_type": "im",
    }
)

# A file_share DM is in scope too (subtype "file_share" passes is_im_message_event).
file_share_im_message_event_body = build_payload(
    {
        "user": "W222",
        "type": "message",
        "subtype": "file_share",
        "ts": "1726133700.887259",
        "text": "uploaded a file",
        "channel": "D111",
        "event_ts": "1726133700.887259",
        "channel_type": "im",
    }
)


class TestAttachingConversationKwargs:
    def test_assistant_event_attaches_kwargs(self):
        middleware = AttachingConversationKwargs()
        req = BoltRequest(body=thread_started_event_body, mode="socket_mode")
        req.context["client"] = WebClient(token="xoxb-test")

        resp = middleware.process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        for key in ASSISTANT_KWARGS:
            assert key in req.context, f"{key} should be set on context"
        assert req.context["say"].thread_ts == "1726133698.626339"
        assert "say_stream" in req.context
        assert "set_status" in req.context

    def test_user_message_event_attaches_kwargs(self):
        middleware = AttachingConversationKwargs()
        req = BoltRequest(body=user_message_event_body, mode="socket_mode")
        req.context["client"] = WebClient(token="xoxb-test")

        resp = middleware.process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        for key in ASSISTANT_KWARGS:
            assert key in req.context, f"{key} should be set on context"
        assert req.context["say"].thread_ts == "1726133698.626339"
        assert "say_stream" in req.context
        assert "set_status" in req.context

    def test_top_level_dm_attaches_suggested_prompts_but_not_set_title(self):
        middleware = AttachingConversationKwargs()
        req = BoltRequest(body=top_level_im_message_event_body, mode="socket_mode")
        req.context["client"] = WebClient(token="xoxb-test")

        resp = middleware.process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        assert "set_suggested_prompts" in req.context
        # set_title is assistant-thread-only; a top-level DM is not an assistant thread
        assert "set_title" not in req.context
        # say/get_thread_context/save_thread_context remain assistant-only
        assert "say" not in req.context
        assert "get_thread_context" not in req.context
        assert "save_thread_context" not in req.context
        # set_status / say_stream are attached whenever a ts is resolvable
        assert "say_stream" in req.context
        assert "set_status" in req.context

    def test_bot_dm_attaches_suggested_prompts(self):
        # set_suggested_prompts is intentionally attached for any IM message, including bot-authored DMs.
        middleware = AttachingConversationKwargs()
        req = BoltRequest(body=bot_im_message_event_body, mode="socket_mode")
        req.context["client"] = WebClient(token="xoxb-test")

        resp = middleware.process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        assert "set_suggested_prompts" in req.context

    def test_file_share_dm_attaches_suggested_prompts(self):
        # A file_share DM is in scope for set_suggested_prompts.
        middleware = AttachingConversationKwargs()
        req = BoltRequest(body=file_share_im_message_event_body, mode="socket_mode")
        req.context["client"] = WebClient(token="xoxb-test")

        resp = middleware.process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        assert "set_suggested_prompts" in req.context

    def test_non_assistant_event_does_not_attach_kwargs(self):
        middleware = AttachingConversationKwargs()
        req = BoltRequest(body=channel_user_message_event_body, mode="socket_mode")
        req.context["client"] = WebClient(token="xoxb-test")

        resp = middleware.process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        for key in ASSISTANT_KWARGS:
            assert key not in req.context, f"{key} should not be set on context"
        assert "say_stream" in req.context
        assert "set_status" in req.context

    def test_non_event_does_not_attach_kwargs(self):
        middleware = AttachingConversationKwargs()
        req = BoltRequest(body="payload={}", headers={})

        resp = middleware.process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        for key in ASSISTANT_KWARGS:
            assert key not in req.context, f"{key} should not be set on context"
        assert "say_stream" not in req.context
        assert "set_status" not in req.context
