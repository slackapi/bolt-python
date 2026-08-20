"""Unit tests for the async outbound recorder (``asyncio_mode = auto``)."""

import time

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.webhook.async_client import AsyncWebhookClient

from slack_bolt.testing.async_recorder import AsyncRecorder


class TestAsyncRecorderPatching:
    def test_patch_installed_and_restored(self):
        original = AsyncWebClient.api_call
        rec = AsyncRecorder()
        rec.start()
        try:
            assert AsyncWebClient.api_call is not original
        finally:
            rec.stop()
        assert AsyncWebClient.api_call is original


class TestAsyncRecorderCapture:
    async def test_records_web_api_call(self):
        rec = AsyncRecorder()
        rec.start()
        try:
            await AsyncWebClient(token="xoxb-x").chat_postMessage(channel="C1", text="hi")
        finally:
            rec.stop()
        found = await rec.wait_for_api_calls("chat.postMessage", text="hi")
        assert len(found) == 1
        assert found[0].kwargs["channel"] == "C1"

    async def test_auth_test_returns_canned_response_with_headers(self):
        rec = AsyncRecorder()
        rec.start()
        try:
            resp = await AsyncWebClient(token="xoxb-x").auth_test()
        finally:
            rec.stop()
        assert resp["ok"] is True
        assert resp.headers["x-oauth-scopes"] == "chat:write,commands"

    async def test_records_respond(self):
        rec = AsyncRecorder()
        rec.start()
        try:
            await AsyncWebhookClient("https://hooks.slack.com/actions/T/1/x").send_dict({"text": "hello"})
        finally:
            rec.stop()
        found = await rec.wait_for_responds(text="hello")
        assert len(found) == 1


class TestAsyncRecorderWaiters:
    async def test_wait_for_api_calls_times_out_returning_empty(self):
        rec = AsyncRecorder()
        start = time.monotonic()
        # Nothing was recorded; the waiter polls the full timeout and returns [].
        found = await rec.wait_for_api_calls("chat.postMessage", timeout=0.2)
        assert found == []
        assert time.monotonic() - start >= 0.2
