"""Unit tests for the sync outbound recorder ("outbox")."""

import threading
import time

from slack_sdk.web.client import WebClient
from slack_sdk.webhook.client import WebhookClient

from slack_bolt.testing.recorder import Recorder


class TestRecorderPatching:
    def test_patch_installed_and_restored(self):
        original = WebClient.api_call
        rec = Recorder()
        rec.start()
        try:
            assert WebClient.api_call is not original
        finally:
            rec.stop()
        assert WebClient.api_call is original


class TestRecorderCapture:
    def test_records_web_api_call_merging_json(self):
        rec = Recorder()
        rec.start()
        try:
            # chat.postMessage routes its payload via json=, others via params=/data=;
            # the recorder must merge them so matching works regardless.
            WebClient(token="xoxb-x").chat_postMessage(channel="C1", text="hi")
        finally:
            rec.stop()
        found = rec.wait_for_api_calls("chat.postMessage", text="hi")
        assert len(found) == 1
        assert found[0].kwargs["channel"] == "C1"

    def test_auth_test_returns_canned_response_with_headers(self):
        rec = Recorder()
        rec.start()
        try:
            resp = WebClient(token="xoxb-x").auth_test()
        finally:
            rec.stop()
        assert resp["ok"] is True
        assert resp["bot_id"] == "B111"
        assert resp.headers["x-oauth-scopes"] == "chat:write,commands"

    def test_records_respond(self):
        rec = Recorder()
        rec.start()
        try:
            WebhookClient("https://hooks.slack.com/actions/T/1/x").send_dict({"text": "hello"})
        finally:
            rec.stop()
        found = rec.wait_for_responds(text="hello")
        assert len(found) == 1
        assert found[0].url == "https://hooks.slack.com/actions/T/1/x"


class TestRecorderWaiters:
    def test_wait_for_api_calls_min_count(self):
        rec = Recorder()
        rec.start()
        try:
            client = WebClient(token="xoxb-x")
            client.chat_postMessage(channel="C1", text="a")
            client.chat_postMessage(channel="C1", text="b")
        finally:
            rec.stop()
        assert len(rec.wait_for_api_calls("chat.postMessage", min_count=2)) == 2

    def test_wait_for_api_calls_times_out_returning_empty(self):
        rec = Recorder()
        start = time.monotonic()
        # Nothing was recorded; the waiter polls the full timeout and returns [].
        found = rec.wait_for_api_calls("chat.postMessage", timeout=0.2)
        assert found == []
        assert time.monotonic() - start >= 0.2

    def test_wait_for_api_calls_polls_for_background_thread_call(self):
        rec = Recorder()
        rec.start()

        def deferred():
            time.sleep(0.15)
            WebClient(token="xoxb-x").chat_postMessage(channel="C1", text="late")

        try:
            threading.Thread(target=deferred).start()
            # The call has not happened yet; the waiter must poll until it lands.
            found = rec.wait_for_api_calls("chat.postMessage", text="late", timeout=1.0)
            assert len(found) == 1
        finally:
            rec.stop()
