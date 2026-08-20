"""The sync test client: the one real-pipeline dispatcher.

:class:`SlackTestClient` encodes a request dataclass the way Slack would send it,
signs it (or opts into socket_mode to skip the signature), wraps it in a real
``BoltRequest``, and runs it through ``app.dispatch`` -- the full
verification + middleware + authorization + listener-matching pipeline. It is a
context manager so the outbound :class:`Recorder` stays patched while background
listener threads finish.
"""

from types import TracebackType
from typing import Optional, Type

from slack_bolt.app.app import App
from slack_bolt.request.request import BoltRequest
from slack_bolt.response import BoltResponse

from .factory import SlackTestRequest
from .internals import build_signed_headers, build_unsigned_headers, encode_wire_body
from .recorder import Recorder


class SlackTestClient:
    """Drive a Bolt ``App`` with faked-but-real inbound requests.

    Args:
        app: the ``App`` under test.
        signing_secret: secret used to sign http-mode requests. Defaults to the
            app's own signing secret so verification passes out of the box.
        recorder: the outbox that captures outbound calls. A fresh
            :class:`Recorder` is created when not supplied.
    """

    def __init__(
        self,
        app: App,
        *,
        signing_secret: Optional[str] = None,
        recorder: Optional[Recorder] = None,
    ) -> None:
        self.app = app
        self.signing_secret = signing_secret if signing_secret is not None else app._signing_secret
        self.recorder = recorder if recorder is not None else Recorder()

    def __enter__(self) -> "SlackTestClient":
        self.recorder.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.recorder.stop()

    def send(self, request: SlackTestRequest, *, verify: bool = True) -> BoltResponse:
        """Dispatch ``request`` through the real pipeline and return the ack ``BoltResponse``.

        With ``verify=True`` (default) the request is signed and dispatched in
        http mode, exercising ``RequestVerification``. With ``verify=False`` it is
        dispatched in socket_mode -- the explicit, documented way to skip the
        signature check; authorization still runs.
        """
        body = request.build_body()
        content_type, raw_body = encode_wire_body(request.wire_format, body)
        if verify:
            headers = build_signed_headers(
                signing_secret=self.signing_secret,
                content_type=content_type,
                raw_body=raw_body,
            )
            bolt_req = BoltRequest(body=raw_body, headers=headers, mode="http")
        else:
            headers = build_unsigned_headers(content_type)
            bolt_req = BoltRequest(body=body, headers=headers, mode="socket_mode")
        return self.app.dispatch(bolt_req)
