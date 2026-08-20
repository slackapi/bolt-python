"""A first-class test client for Bolt apps.

Drive an ``App`` / ``AsyncApp`` with faked-but-real inbound requests: build the
payload Slack would send, sign it, and run it through the app's real
``dispatch`` pipeline (verification + middleware + authorization + listener
matching). The outbound :class:`Recorder` ("outbox") captures the ``say`` /
``respond`` / Web API calls the app makes so tests can assert on them.

Example::

    from slack_bolt.testing import SlackTestClient, SlackRequestFactory

    f = SlackRequestFactory()
    with SlackTestClient(app) as client:
        resp = client.send(f.command("/hi", text="world"))
        assert resp.status == 200
        assert len(client.recorder.wait_for_api_calls("chat.postMessage", text="Hi!")) == 1

This package stays sync-clean: importing it never pulls in ``aiohttp``. The async
twins live in dedicated modules and are imported directly --
:class:`AsyncSlackTestClient` from ``slack_bolt.testing.async_client`` and
:class:`AsyncRecorder` from ``slack_bolt.testing.async_recorder`` -- mirroring how
``AsyncApp`` lives at ``slack_bolt.app.async_app``. They share this package's
factory and request dataclasses unchanged.
"""

from .client import SlackTestClient
from .factory import (
    ActionRequest,
    CommandRequest,
    EventRequest,
    FunctionRequest,
    OptionsRequest,
    ShortcutRequest,
    SlackRequestFactory,
    SlackTestRequest,
    ViewClosedRequest,
    ViewSubmissionRequest,
)
from .internals import WireFormat
from .recorder import RecordedApiCall, RecordedRespond, Recorder

__all__ = [
    "SlackTestClient",
    "SlackRequestFactory",
    "SlackTestRequest",
    "WireFormat",
    "CommandRequest",
    "EventRequest",
    "ActionRequest",
    "ShortcutRequest",
    "ViewSubmissionRequest",
    "ViewClosedRequest",
    "OptionsRequest",
    "FunctionRequest",
    "Recorder",
    "RecordedApiCall",
    "RecordedRespond",
]
