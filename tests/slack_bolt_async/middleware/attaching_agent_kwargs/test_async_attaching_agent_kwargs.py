import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.middleware.attaching_agent_kwargs.async_attaching_agent_kwargs import AsyncAttachingAgentKwargs
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from tests.scenario_tests_async.test_events_assistant import (
    thread_started_event_body,
    user_message_event_body,
    channel_user_message_event_body,
)


async def next():
    return BoltResponse(status=200)


AGENT_KWARGS = ("say", "set_status", "set_title", "set_suggested_prompts", "get_thread_context", "save_thread_context")


class TestAsyncAttachingAgentKwargs:
    @pytest.mark.asyncio
    async def test_assistant_event_attaches_kwargs(self):
        middleware = AsyncAttachingAgentKwargs()
        req = AsyncBoltRequest(body=thread_started_event_body, mode="socket_mode")
        req.context["client"] = AsyncWebClient(token="xoxb-test")
        resp = BoltResponse(status=404)

        resp = await middleware.async_process(req=req, resp=resp, next=next)

        assert resp.status == 200
        for key in AGENT_KWARGS:
            assert key in req.context, f"{key} should be set on context"
        assert req.context["say"].thread_ts == "1726133698.626339"

    @pytest.mark.asyncio
    async def test_user_message_assistant_event_attaches_kwargs(self):
        middleware = AsyncAttachingAgentKwargs()
        req = AsyncBoltRequest(body=user_message_event_body, mode="socket_mode")
        req.context["client"] = AsyncWebClient(token="xoxb-test")
        resp = BoltResponse(status=404)

        resp = await middleware.async_process(req=req, resp=resp, next=next)

        assert resp.status == 200
        for key in AGENT_KWARGS:
            assert key in req.context, f"{key} should be set on context"
        assert req.context["say"].thread_ts == "1726133698.626339"

    @pytest.mark.asyncio
    async def test_non_assistant_event_does_not_attach_kwargs(self):
        middleware = AsyncAttachingAgentKwargs()
        req = AsyncBoltRequest(body=channel_user_message_event_body, mode="socket_mode")
        req.context["client"] = AsyncWebClient(token="xoxb-test")
        resp = BoltResponse(status=404)

        resp = await middleware.async_process(req=req, resp=resp, next=next)

        assert resp.status == 200
        for key in AGENT_KWARGS:
            assert key not in req.context, f"{key} should not be set on context"

    @pytest.mark.asyncio
    async def test_non_event_body_does_not_attach_kwargs(self):
        middleware = AsyncAttachingAgentKwargs()
        req = AsyncBoltRequest(body="payload={}", headers={})
        resp = BoltResponse(status=404)

        resp = await middleware.async_process(req=req, resp=resp, next=next)

        assert resp.status == 200
        for key in AGENT_KWARGS:
            assert key not in req.context, f"{key} should not be set on context"

    @pytest.mark.asyncio
    async def test_next_always_called(self):
        middleware = AsyncAttachingAgentKwargs()
        call_state = {"called": False}

        async def tracking_next():
            call_state["called"] = True
            return BoltResponse(status=200)

        # With assistant event
        req = AsyncBoltRequest(body=thread_started_event_body, mode="socket_mode")
        req.context["client"] = AsyncWebClient(token="xoxb-test")
        await middleware.async_process(req=req, resp=BoltResponse(status=404), next=tracking_next)
        assert call_state["called"] is True

        # With non-event body
        call_state["called"] = False
        req = AsyncBoltRequest(body="payload={}", headers={})
        await middleware.async_process(req=req, resp=BoltResponse(status=404), next=tracking_next)
        assert call_state["called"] is True
