import asyncio
from typing import Any, Dict, Optional, Sequence

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest

from . import payloads
from .mock_slack_server import MockSlackServer
from .client import DispatchResult, _BaseTestClient


class AsyncBoltTestClient(_BaseTestClient):
    """Sends signed requests to a Bolt `AsyncApp` in tests and reports what the app did.

    This is the `AsyncApp` counterpart of `BoltTestClient`. After the app acknowledges a request,
    the client waits for the listener and lazy listener tasks it started, so all of their side
    effects are done when a call returns.
    """

    def __init__(self, app: AsyncApp, server: MockSlackServer, *, timeout: float = 10.0):
        self.app = app
        self.server = server
        self.signing_secret = app._signing_secret
        self.timeout = timeout
        app.client.base_url = server.base_url

    async def dispatch(self, payload: Dict[str, Any], *, headers: Optional[Dict[str, str]] = None) -> DispatchResult:
        """Dispatches a payload (e.g. built with `slack_bolt.testing.payloads`) to the app."""
        body, request_headers = self._prepare(payload, headers)
        calls_before = len(self.server.calls)
        responds_before = len(self.server.responds)
        existing = asyncio.all_tasks()
        response = await self.app.async_dispatch(AsyncBoltRequest(body=body, headers=request_headers))
        await self._wait_for_started_tasks(existing)
        return DispatchResult(
            response=response,
            api_calls=self.server.calls[calls_before:],
            responds=self.server.responds[responds_before:],
        )

    async def _wait_for_started_tasks(self, existing) -> None:
        loop = asyncio.get_event_loop()
        deadline = loop.time() + self.timeout
        current = asyncio.current_task()
        while True:
            pending = [t for t in asyncio.all_tasks() if t not in existing and t is not current and not t.done()]
            if not pending:
                return
            remaining = deadline - loop.time()
            if remaining <= 0:
                raise asyncio.TimeoutError(f"Listener tasks did not finish within {self.timeout} seconds")
            await asyncio.wait(pending, timeout=remaining)

    async def event(self, event: Dict[str, Any], **kwargs: Any) -> DispatchResult:
        """Sends an Events API request with the given event, e.g. `{"type": "app_mention", ...}`."""
        return await self.dispatch(payloads.event(event, **kwargs))

    async def message(self, text: str, **kwargs: Any) -> DispatchResult:
        """Sends a `message` event."""
        return await self.dispatch(payloads.message(text, **kwargs))

    async def slash_command(self, command: str, text: str = "", **kwargs: Any) -> DispatchResult:
        """Sends a slash command. `respond()` calls are recorded in the result."""
        return await self.dispatch(payloads.slash_command(command, text, **self._with_response_url(kwargs)))

    async def block_action(self, action_id: str, **kwargs: Any) -> DispatchResult:
        """Sends a `block_actions` request. `respond()` calls are recorded in the result."""
        return await self.dispatch(payloads.block_action(action_id, **self._with_response_url(kwargs)))

    async def shortcut(self, callback_id: str, **kwargs: Any) -> DispatchResult:
        """Sends a global shortcut."""
        return await self.dispatch(payloads.shortcut(callback_id, **kwargs))

    async def message_shortcut(self, callback_id: str, **kwargs: Any) -> DispatchResult:
        """Sends a message shortcut. `respond()` calls are recorded in the result."""
        return await self.dispatch(payloads.message_shortcut(callback_id, **self._with_response_url(kwargs)))

    async def view_submission(
        self,
        callback_id: str,
        values: Optional[Dict[str, Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> DispatchResult:
        """Sends a `view_submission` request for a modal."""
        return await self.dispatch(payloads.view_submission(callback_id, values, **kwargs))


__all__: Sequence[str] = ["AsyncBoltTestClient"]
