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

    def test_send_response_text_starting_with_brace(self):
        # A text ack that happens to start with "{" is not JSON and must be sent as text
        from slack_bolt.adapter.socket_mode.internals import send_response
        from slack_bolt.response import BoltResponse
        import logging

        sent = []

        class FakeClient:
            logger = logging.getLogger("test")

            def send_socket_mode_response(self, response):
                sent.append(response)

        req = SocketModeRequest(type="slash_commands", envelope_id="e1", payload={"command": "/echo"})
        send_response(FakeClient(), req, BoltResponse(status=200, body="{foo"), 0.0)
        assert len(sent) == 1
        assert sent[0].payload == {"text": "{foo"}

        sent.clear()
        send_response(FakeClient(), req, BoltResponse(status=200, body='{"text": "hi"}'), 0.0)
        assert sent[0].payload == {"text": "hi"}
