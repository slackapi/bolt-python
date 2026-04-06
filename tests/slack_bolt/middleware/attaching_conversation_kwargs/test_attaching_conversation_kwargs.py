from slack_sdk import WebClient

from slack_bolt.middleware.attaching_conversation_kwargs import AttachingConversationKwargs
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from tests.scenario_tests.test_events_assistant import (
    thread_started_event_body,
    user_message_event_body,
    channel_user_message_event_body,
)


def next():
    return BoltResponse(status=200)


ASSISTANT_KWARGS = ("say", "set_title", "set_suggested_prompts", "get_thread_context", "save_thread_context")


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
