"""Async twin of :class:`slack_bolt.testing.client.SlackTestClient`.

Same shape, awaited: an ``async with`` context manager whose ``async def send``
awaits ``app.async_dispatch``. It consumes the very same shared
:class:`SlackRequestFactory` and request dataclasses as the sync client -- only
the dispatch entry point and the outbox seam differ.
"""

from types import TracebackType
from typing import Optional, Type

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse

from .async_recorder import AsyncRecorder
from .factory import SlackTestRequest
from .internals import build_signed_headers, build_unsigned_headers, encode_wire_body


class AsyncSlackTestClient:
    """Drive an ``AsyncApp`` with faked-but-real inbound requests.

    Args:
        app: the ``AsyncApp`` under test.
        signing_secret: secret used to sign http-mode requests. Defaults to the
            app's own signing secret so verification passes out of the box.
        recorder: the outbox that captures outbound calls. A fresh
            :class:`AsyncRecorder` is created when not supplied.
    """

    def __init__(
        self,
        app: AsyncApp,
        *,
        signing_secret: Optional[str] = None,
        recorder: Optional[AsyncRecorder] = None,
    ) -> None:
        self.app = app
        self.signing_secret = signing_secret if signing_secret is not None else app._signing_secret
        self.recorder = recorder if recorder is not None else AsyncRecorder()

    async def __aenter__(self) -> "AsyncSlackTestClient":
        self.recorder.start()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.recorder.stop()

    async def send(self, request: SlackTestRequest, *, verify: bool = True) -> BoltResponse:
        """Dispatch ``request`` through the real async pipeline and return the ack ``BoltResponse``.

        With ``verify=True`` (default) the request is signed and dispatched in
        http mode. With ``verify=False`` it is dispatched in socket_mode -- the
        explicit way to skip the signature check; authorization still runs.
        """
        body = request.build_body()
        content_type, raw_body = encode_wire_body(request.wire_format, body)
        if verify:
            headers = build_signed_headers(
                signing_secret=self.signing_secret,
                content_type=content_type,
                raw_body=raw_body,
            )
            bolt_req = AsyncBoltRequest(body=raw_body, headers=headers, mode="http")
        else:
            headers = build_unsigned_headers(content_type)
            bolt_req = AsyncBoltRequest(body=body, headers=headers, mode="socket_mode")
        return await self.app.async_dispatch(bolt_req)
