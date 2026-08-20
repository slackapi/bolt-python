"""Outbound recorder ("outbox") for the sync test client.

A Slack app's real output is not its HTTP response -- it is the *outbound* calls it
makes: ``say()`` / ``client.*`` (Web API) and ``respond()`` (response_url webhook).
The recorder intercepts both at the shared ``slack_sdk`` class seam, records them
in-process, and returns canned responses so nothing hits the network. The
``wait_for_*`` methods poll (default 1s) because the default ``App`` runs listener
bodies on a background thread after ``ack`` returns; they return the matched calls
and leave the assertion to the caller.

``_RecorderStore`` holds the client-agnostic pieces (thread-safe storage, matching)
so the async recorder can reuse them; :class:`Recorder` adds the sync patching.
"""

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from unittest.mock import patch

from slack_sdk.web import SlackResponse
from slack_sdk.web.client import WebClient
from slack_sdk.webhook.client import WebhookClient
from slack_sdk.webhook.webhook_response import WebhookResponse

# Shared by the sync and async waiters (async_recorder imports these).
_POLL_INTERVAL = 0.05
_DEFAULT_TIMEOUT = 1.0

# Canned auth.test so MultiTeams/SingleTeam authorization passes without a network call.
DEFAULT_AUTH_TEST_DATA: Dict[str, Any] = {
    "ok": True,
    "url": "https://test.slack.com/",
    "team": "Test Team",
    "user": "test_bot",
    "team_id": "T111",
    "user_id": "UB111",
    "bot_id": "B111",
    "is_enterprise_install": False,
}
DEFAULT_AUTH_TEST_HEADERS: Dict[str, str] = {"x-oauth-scopes": "chat:write,commands"}


@dataclass
class RecordedApiCall:
    """A captured Web API call, e.g. from ``say()`` or a direct ``client.*`` call."""

    api_method: str
    kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RecordedRespond:
    """A captured ``respond()`` call to a response_url webhook."""

    url: str
    body: Dict[str, Any] = field(default_factory=dict)


def _matches(recorded: Dict[str, Any], matchers: Dict[str, Any]) -> bool:
    return all(recorded.get(key) == value for key, value in matchers.items())


def _merge_api_call_kwargs(data: Any, params: Any, json: Any) -> Dict[str, Any]:
    # A Web API payload lands in exactly one of data/params/json depending on the
    # method; merge them so assertions can match regardless of which was used.
    merged: Dict[str, Any] = {}
    for candidate in (data, params, json):
        if isinstance(candidate, dict):
            merged.update(candidate)
    return merged


class _RecorderStore:
    """Thread-safe storage + matching shared by the sync and async recorders."""

    def __init__(
        self,
        *,
        auth_test_data: Optional[Dict[str, Any]] = None,
        auth_test_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self._lock = threading.Lock()
        self._api_calls: List[RecordedApiCall] = []
        self._responds: List[RecordedRespond] = []
        self.auth_test_data = auth_test_data if auth_test_data is not None else dict(DEFAULT_AUTH_TEST_DATA)
        self.auth_test_headers = auth_test_headers if auth_test_headers is not None else dict(DEFAULT_AUTH_TEST_HEADERS)

    # -- recording (called from the listener thread) --

    def _record_api_call(self, api_method: str, kwargs: Dict[str, Any]) -> None:
        with self._lock:
            self._api_calls.append(RecordedApiCall(api_method, dict(kwargs)))

    def _record_respond(self, url: str, body: Dict[str, Any]) -> None:
        with self._lock:
            self._responds.append(RecordedRespond(url, dict(body)))

    # -- reading (called from the test thread) --

    @property
    def api_calls(self) -> List[RecordedApiCall]:
        with self._lock:
            return list(self._api_calls)

    @property
    def responds(self) -> List[RecordedRespond]:
        with self._lock:
            return list(self._responds)

    def _find_api_calls(self, api_method: str, matchers: Dict[str, Any]) -> List[RecordedApiCall]:
        return [c for c in self.api_calls if c.api_method == api_method and _matches(c.kwargs, matchers)]

    def _find_responds(self, matchers: Dict[str, Any]) -> List[RecordedRespond]:
        return [r for r in self.responds if _matches(r.body, matchers)]

    def _auth_test_response_data(self, api_method: str) -> Dict[str, Any]:
        return dict(self.auth_test_data) if api_method == "auth.test" else {"ok": True}

    def _auth_test_response_headers(self, api_method: str) -> Dict[str, str]:
        return dict(self.auth_test_headers) if api_method == "auth.test" else {}


class Recorder(_RecorderStore):
    """Sync outbox: patches ``WebClient.api_call`` and ``WebhookClient.send_dict``."""

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

        def patched_api_call(
            client_self: WebClient,
            api_method: str,
            *,
            http_verb: str = "POST",
            files: Any = None,
            data: Any = None,
            params: Any = None,
            json: Any = None,
            headers: Any = None,
            auth: Any = None,
        ) -> SlackResponse:
            merged = _merge_api_call_kwargs(data, params, json)
            recorder._record_api_call(api_method, merged)
            return SlackResponse(
                client=client_self,
                http_verb=http_verb,
                api_url=f"https://slack.com/api/{api_method}",
                req_args={},
                data=recorder._auth_test_response_data(api_method),
                headers=recorder._auth_test_response_headers(api_method),
                status_code=200,
            )

        def patched_send_dict(
            client_self: WebhookClient,
            body: Dict[str, Any],
            headers: Optional[Dict[str, str]] = None,
        ) -> WebhookResponse:
            recorder._record_respond(client_self.url, body)
            return WebhookResponse(url=client_self.url, status_code=200, body="ok", headers={})

        self._patchers = [
            patch.object(WebClient, "api_call", patched_api_call),
            patch.object(WebhookClient, "send_dict", patched_send_dict),
        ]
        for p in self._patchers:
            p.start()

    def stop(self) -> None:
        for p in reversed(self._patchers):
            p.stop()
        self._patchers.clear()

    # -- waiters (poll because listener bodies run on a background thread) --

    def _poll(
        self,
        query: Callable[[], List[Any]],
        *,
        min_count: int,
        timeout: float,
    ) -> List[Any]:
        # Block until ``query()`` returns at least ``min_count`` items or ``timeout``
        # elapses, then return whatever it found (possibly fewer). monotonic() so an
        # NTP step can't stretch or shrink the deadline.
        deadline = time.monotonic() + timeout
        while True:
            found = query()
            if len(found) >= min_count or time.monotonic() >= deadline:
                return found
            time.sleep(_POLL_INTERVAL)

    def wait_for_api_calls(
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
        return self._poll(
            lambda: self._find_api_calls(api_method, matchers),
            min_count=min_count,
            timeout=timeout,
        )

    def wait_for_responds(
        self, *, min_count: int = 1, timeout: float = _DEFAULT_TIMEOUT, **matchers: Any
    ) -> List[RecordedRespond]:
        """Wait for and return ``respond()`` calls matching ``matchers``.

        Same polling contract as :meth:`wait_for_api_calls`; the caller asserts.
        """
        return self._poll(
            lambda: self._find_responds(matchers),
            min_count=min_count,
            timeout=timeout,
        )
