from slack_sdk.socket_mode.request import SocketModeRequest

from slack_bolt.adapter.socket_mode.internals import build_headers, run_bolt_app


class TestSocketModeInternals:
    def test_build_retry_headers_without_retry(self):
        req = SocketModeRequest(type="events_api", envelope_id="e1", payload={"type": "event_callback"})
        assert build_headers(req) is None

    def test_build_retry_headers_with_retry(self):
        req = SocketModeRequest(
            type="events_api",
            envelope_id="e1",
            payload={"type": "event_callback"},
            retry_attempt=2,
            retry_reason="http_timeout",
        )
        headers = build_headers(req)
        assert headers == {"x-slack-retry-num": "2", "x-slack-retry-reason": "http_timeout"}
