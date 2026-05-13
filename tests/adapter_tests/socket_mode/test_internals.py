from slack_sdk.socket_mode.request import SocketModeRequest

from slack_bolt.adapter.socket_mode.internals import build_retry_headers, run_bolt_app


class TestSocketModeInternals:
    def test_build_retry_headers_without_retry(self):
        req = SocketModeRequest(type="events_api", envelope_id="e1", payload={"type": "event_callback"})
        assert build_retry_headers(req) is None

    def test_build_retry_headers_with_retry(self):
        req = SocketModeRequest(
            type="events_api",
            envelope_id="e1",
            payload={"type": "event_callback"},
            retry_attempt=2,
            retry_reason="http_timeout",
        )
        headers = build_retry_headers(req)
        assert headers == {"x-slack-retry-num": "2", "x-slack-retry-reason": "http_timeout"}

    def test_run_bolt_app_propagates_retry_headers(self):
        captured = {}

        class FakeApp:
            def dispatch(self, bolt_req):
                captured["headers"] = bolt_req.headers
                return None

        req = SocketModeRequest(
            type="events_api",
            envelope_id="e1",
            payload={"type": "event_callback", "event": {"type": "app_mention"}},
            retry_attempt=1,
            retry_reason="http_timeout",
        )
        run_bolt_app(FakeApp(), req)
        assert captured["headers"]["x-slack-retry-num"] == ["1"]
        assert captured["headers"]["x-slack-retry-reason"] == ["http_timeout"]
