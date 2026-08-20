"""Async twin of :class:`slack_bolt.testing.recorder.Recorder`.

Identical behavior, patched at the async ``slack_sdk`` seams and exposing the
``wait_for_*`` surface as ``async def`` methods that poll with ``await
asyncio.sleep``. It reuses the client-agnostic :class:`_RecorderStore` from the
sync module (the sync module imports only ``slack_sdk``'s sync clients, never
``aiohttp``, so the async path can safely depend on it -- the reverse would not
hold).
"""

import asyncio
import time
from typing import Any, Callable, Dict, List, Optional
from unittest.mock import patch

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse
from slack_sdk.webhook.async_client import AsyncWebhookClient
from slack_sdk.webhook.webhook_response import WebhookResponse

from .recorder import (
    _DEFAULT_TIMEOUT,
    _POLL_INTERVAL,
    RecordedApiCall,
    RecordedRespond,
    _merge_api_call_kwargs,
    _RecorderStore,
)


class AsyncRecorder(_RecorderStore):
    """Async outbox: patches ``AsyncWebClient.api_call`` and ``AsyncWebhookClient.send_dict``."""

    def __init__(
        self,
        *,
        auth_test_data: Optional[Dict[str, Any]] = None,
        auth_test_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(auth_test_data=auth_test_data, auth_test_headers=auth_test_headers)
        self._patchers: List[Any] = []

    def start(self) -> None:
        recorder = self

        async def patched_api_call(
            client_self: AsyncWebClient,
            api_method: str,
            *,
            http_verb: str = "POST",
            files: Any = None,
            data: Any = None,
            params: Any = None,
            json: Any = None,
            headers: Any = None,
            auth: Any = None,
        ) -> AsyncSlackResponse:
            merged = _merge_api_call_kwargs(data, params, json)
            recorder._record_api_call(api_method, merged)
            return AsyncSlackResponse(
                client=client_self,
                http_verb=http_verb,
                api_url=f"https://slack.com/api/{api_method}",
                req_args={},
                data=recorder._auth_test_response_data(api_method),
                headers=recorder._auth_test_response_headers(api_method),
                status_code=200,
            )

        async def patched_send_dict(
            client_self: AsyncWebhookClient,
            body: Dict[str, Any],
            headers: Optional[Dict[str, str]] = None,
        ) -> WebhookResponse:
            recorder._record_respond(client_self.url, body)
            return WebhookResponse(url=client_self.url, status_code=200, body="ok", headers={})

        self._patchers = [
            patch.object(AsyncWebClient, "api_call", patched_api_call),
            patch.object(AsyncWebhookClient, "send_dict", patched_send_dict),
        ]
        for p in self._patchers:
            p.start()

    def stop(self) -> None:
        for p in reversed(self._patchers):
            p.stop()
        self._patchers.clear()

    # -- waiters (poll because listener bodies may run as lazy tasks) --

    async def _poll(
        self,
        query: Callable[[], List[Any]],
        *,
        min_count: int,
        timeout: float,
    ) -> List[Any]:
        # Block until ``query()`` returns at least ``min_count`` items or ``timeout``
        # elapses, then return whatever it found (possibly fewer). ``query`` reads the
        # in-memory store (no I/O), so it needs no await. monotonic() so an NTP step
        # can't stretch or shrink the deadline.
        deadline = time.monotonic() + timeout
        while True:
            found = query()
            if len(found) >= min_count or time.monotonic() >= deadline:
                return found
            await asyncio.sleep(_POLL_INTERVAL)

    async def wait_for_api_calls(
        self,
        api_method: str,
        *,
        min_count: int = 1,
        timeout: float = _DEFAULT_TIMEOUT,
        **matchers: Any,
    ) -> List[RecordedApiCall]:
        """Wait for and return Web API calls to ``api_method`` matching ``matchers``.

        Polls until at least ``min_count`` matches are recorded or ``timeout`` seconds
        pass, then returns them (possibly fewer than ``min_count`` on timeout, or an
        empty list -- useful for a "nothing was sent" check). The caller asserts.
        """
        return await self._poll(
            lambda: self._find_api_calls(api_method, matchers),
            min_count=min_count,
            timeout=timeout,
        )

    async def wait_for_responds(
        self, *, min_count: int = 1, timeout: float = _DEFAULT_TIMEOUT, **matchers: Any
    ) -> List[RecordedRespond]:
        """Wait for and return ``respond()`` calls matching ``matchers``.

        Same polling contract as :meth:`wait_for_api_calls`; the caller asserts.
        """
        return await self._poll(
            lambda: self._find_responds(matchers),
            min_count=min_count,
            timeout=timeout,
        )
