import logging

import pytest
from slack_sdk.socket_mode.request import SocketModeRequest

from slack_bolt.adapter.socket_mode.async_internals import send_async_response
from slack_bolt.response import BoltResponse


class TestAsyncSocketModeInternals:
    @pytest.mark.asyncio
    async def test_send_response_text_starting_with_brace(self):
        # A text ack that happens to start with "{" is not JSON and must be sent as text
        sent = []

        class FakeClient:
            logger = logging.getLogger("test")

            async def send_socket_mode_response(self, response):
                sent.append(response)

        req = SocketModeRequest(type="slash_commands", envelope_id="e1", payload={"command": "/echo"})
        await send_async_response(FakeClient(), req, BoltResponse(status=200, body="{foo"), 0.0)
        assert len(sent) == 1
        assert sent[0].payload == {"text": "{foo"}

        sent.clear()
        await send_async_response(FakeClient(), req, BoltResponse(status=200, body='{"text": "hi"}'), 0.0)
        assert sent[0].payload == {"text": "hi"}
