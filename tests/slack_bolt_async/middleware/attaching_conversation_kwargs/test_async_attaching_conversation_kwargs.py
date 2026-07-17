import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.middleware.attaching_conversation_kwargs.async_attaching_conversation_kwargs import (
    AsyncAttachingConversationKwargs,
)
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from tests.scenario_tests_async.test_events_assistant import (
    build_payload,
    thread_started_event_body,
    user_message_event_body,
    channel_user_message_event_body,
)


async def next():
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

# Opening the Messages tab of App Home is in scope for set_suggested_prompts.
app_home_opened_messages_event_body = build_payload(
    {
        "type": "app_home_opened",
        "user": "W222",
        "channel": "D111",
        "tab": "messages",
        "event_ts": "1726133700.887259",
    }
)

# Opening the Home tab is NOT in scope: set_suggested_prompts should not be attached.
app_home_opened_home_event_body = build_payload(
    {
        "type": "app_home_opened",
        "user": "W222",
        "channel": "D111",
        "tab": "home",
        "event_ts": "1726133700.887259",
    }
)


class TestAsyncAttachingConversationKwargs:
    @pytest.mark.asyncio
    async def test_assistant_event_attaches_kwargs(self):
        middleware = AsyncAttachingConversationKwargs()
        req = AsyncBoltRequest(body=thread_started_event_body, mode="socket_mode")
        req.context["client"] = AsyncWebClient(token="xoxb-test")

        resp = await middleware.async_process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        for key in ASSISTANT_KWARGS:
            assert key in req.context, f"{key} should be set on context"
        assert req.context["say"].thread_ts == "1726133698.626339"
        assert "say_stream" in req.context
        assert "set_status" in req.context

    @pytest.mark.asyncio
    async def test_user_message_event_attaches_kwargs(self):
        middleware = AsyncAttachingConversationKwargs()
        req = AsyncBoltRequest(body=user_message_event_body, mode="socket_mode")
        req.context["client"] = AsyncWebClient(token="xoxb-test")

        resp = await middleware.async_process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        for key in ASSISTANT_KWARGS:
            assert key in req.context, f"{key} should be set on context"
        assert req.context["say"].thread_ts == "1726133698.626339"
        assert "say_stream" in req.context
        assert "set_status" in req.context

    @pytest.mark.asyncio
    async def test_top_level_dm_attaches_suggested_prompts_but_not_set_title(self):
        middleware = AsyncAttachingConversationKwargs()
        req = AsyncBoltRequest(body=top_level_im_message_event_body, mode="socket_mode")
        req.context["client"] = AsyncWebClient(token="xoxb-test")

        resp = await middleware.async_process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        assert "set_suggested_prompts" in req.context
        assert "set_title" not in req.context
        assert "say" not in req.context
        assert "get_thread_context" not in req.context
        assert "save_thread_context" not in req.context
        assert "say_stream" in req.context
        assert "set_status" in req.context

    @pytest.mark.asyncio
    async def test_bot_dm_attaches_suggested_prompts(self):
        middleware = AsyncAttachingConversationKwargs()
        req = AsyncBoltRequest(body=bot_im_message_event_body, mode="socket_mode")
        req.context["client"] = AsyncWebClient(token="xoxb-test")

        resp = await middleware.async_process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        assert "set_suggested_prompts" in req.context

    @pytest.mark.asyncio
    async def test_file_share_dm_attaches_suggested_prompts(self):
        middleware = AsyncAttachingConversationKwargs()
        req = AsyncBoltRequest(body=file_share_im_message_event_body, mode="socket_mode")
        req.context["client"] = AsyncWebClient(token="xoxb-test")

        resp = await middleware.async_process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        assert "set_suggested_prompts" in req.context

    @pytest.mark.asyncio
    async def test_app_home_opened_messages_tab_attaches_suggested_prompts(self):
        middleware = AsyncAttachingConversationKwargs()
        req = AsyncBoltRequest(body=app_home_opened_messages_event_body, mode="socket_mode")
        req.context["client"] = AsyncWebClient(token="xoxb-test")

        resp = await middleware.async_process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        assert "set_suggested_prompts" in req.context
        assert "say" not in req.context
        assert "set_title" not in req.context
        assert "get_thread_context" not in req.context
        assert "save_thread_context" not in req.context

    @pytest.mark.asyncio
    async def test_app_home_opened_home_tab_does_not_attach_suggested_prompts(self):
        middleware = AsyncAttachingConversationKwargs()
        req = AsyncBoltRequest(body=app_home_opened_home_event_body, mode="socket_mode")
        req.context["client"] = AsyncWebClient(token="xoxb-test")

        resp = await middleware.async_process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        assert "set_suggested_prompts" not in req.context

    @pytest.mark.asyncio
    async def test_non_assistant_event_does_not_attach_kwargs(self):
        middleware = AsyncAttachingConversationKwargs()
        req = AsyncBoltRequest(body=channel_user_message_event_body, mode="socket_mode")
        req.context["client"] = AsyncWebClient(token="xoxb-test")

        resp = await middleware.async_process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        for key in ASSISTANT_KWARGS:
            assert key not in req.context, f"{key} should not be set on context"
        assert "say_stream" in req.context
        assert "set_status" in req.context

    @pytest.mark.asyncio
    async def test_non_event_does_not_attach_kwargs(self):
        middleware = AsyncAttachingConversationKwargs()
        req = AsyncBoltRequest(body="payload={}", headers={})

        resp = await middleware.async_process(req=req, resp=BoltResponse(status=404), next=next)

        assert resp.status == 200
        for key in ASSISTANT_KWARGS:
            assert key not in req.context, f"{key} should not be set on context"
        assert "say_stream" not in req.context
        assert "set_status" not in req.context
