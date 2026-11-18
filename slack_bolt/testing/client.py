import json
from concurrent.futures import Executor, Future
from typing import Any, Callable, Dict, List, Optional, Sequence

from slack_bolt.app import App
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse

from . import payloads
from .mock_slack_server import APICall, MockSlackServer


class InlineExecutor(Executor):
    """An executor that runs each submitted function immediately in the calling thread."""

    def submit(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Future:  # type: ignore[override]
        future: Future = Future()
        try:
            future.set_result(fn(*args, **kwargs))
        except BaseException as e:
            future.set_exception(e)
        return future


class DispatchResult:
    """The outcome of dispatching one request to a Bolt app in a test."""

    response: Optional[BoltResponse]
    """The HTTP response the app returned to Slack, or None if no listener acknowledged the request."""
    api_calls: List[APICall]
    """The Web API calls the app made while handling this request."""
    responds: List[Dict[str, Any]]
    """The messages the app posted to the request's `response_url` (e.g. with `respond()`)."""

    def __init__(
        self,
        *,
        response: Optional[BoltResponse],
        api_calls: List[APICall],
        responds: List[Dict[str, Any]],
    ):
        self.response = response
        self.api_calls = api_calls
        self.responds = responds

    @property
    def status(self) -> Optional[int]:
        """The HTTP status of the response, or None if no listener acknowledged the request."""
        return self.response.status if self.response is not None else None

    @property
    def body(self) -> str:
        """The raw response body, e.g. the text passed to `ack()`."""
        return self.response.body if self.response is not None else ""

    @property
    def json(self) -> Optional[Dict[str, Any]]:
        """The response body parsed as JSON, or None if it is empty or not JSON."""
        try:
            parsed = json.loads(self.body)
        except ValueError:
            return None
        return parsed if isinstance(parsed, dict) else None

    def calls_to(self, method: str) -> List[APICall]:
        """The Web API calls made for the given method while handling this request."""
        return [c for c in self.api_calls if c.method == method]

    def __repr__(self) -> str:
        return f"DispatchResult(status={self.status!r}, body={self.body!r}, api_calls={self.api_calls!r})"


class _BaseTestClient:
    server: MockSlackServer
    signing_secret: str

    def _prepare(self, payload: Dict[str, Any], headers: Optional[Dict[str, str]]):
        body = payloads.to_http_body(payload)
        request_headers = payloads.signed_headers(body, self.signing_secret)
        request_headers.update(headers or {})
        return body, request_headers

    def _with_response_url(self, kwargs: Dict[str, Any], key: str = "response_url") -> Dict[str, Any]:
        kwargs.setdefault(key, self.server.response_url())
        return kwargs


class BoltTestClient(_BaseTestClient):
    """Sends signed requests to a Bolt `App` in tests and reports what the app did.

        server = MockSlackServer().start()
        app = App(client=server.web_client("xoxb-test"), signing_secret="secret")

        @app.command("/hello")
        def hello(ack, respond):
            ack()
            respond("Hi!")

        result = BoltTestClient(app, server).slash_command("/hello")
        assert result.status == 200
        assert result.responds == [{"text": "Hi!"}]

    Requests run through the app's full middleware chain, including request verification
    and authorization. The test client points the app's Web API client at `server`, and runs
    listeners and lazy listeners in the calling thread, so all of their side effects are done
    when a call returns, even when `process_before_response` is False.
    """

    def __init__(self, app: App, server: MockSlackServer):
        self.app = app
        self.server = server
        self.signing_secret = app._signing_secret
        app.client.base_url = server.base_url
        executor = InlineExecutor()
        app.listener_runner.listener_executor = executor
        app.listener_runner.lazy_listener_runner.executor = executor  # type: ignore[attr-defined]

    def dispatch(self, payload: Dict[str, Any], *, headers: Optional[Dict[str, str]] = None) -> DispatchResult:
        """Dispatches a payload (e.g. built with `slack_bolt.testing.payloads`) to the app."""
        body, request_headers = self._prepare(payload, headers)
        calls_before = len(self.server.calls)
        responds_before = len(self.server.responds)
        response = self.app.dispatch(BoltRequest(body=body, headers=request_headers))
        return DispatchResult(
            response=response,
            api_calls=self.server.calls[calls_before:],
            responds=self.server.responds[responds_before:],
        )

    def event(self, event: Dict[str, Any], **kwargs: Any) -> DispatchResult:
        """Sends an Events API request with the given event, e.g. `{"type": "app_mention", ...}`."""
        return self.dispatch(payloads.event(event, **kwargs))

    def message(self, text: str, **kwargs: Any) -> DispatchResult:
        """Sends a `message` event."""
        return self.dispatch(payloads.message(text, **kwargs))

    def slash_command(self, command: str, text: str = "", **kwargs: Any) -> DispatchResult:
        """Sends a slash command. `respond()` calls are recorded in the result."""
        return self.dispatch(payloads.slash_command(command, text, **self._with_response_url(kwargs)))

    def block_action(self, action_id: str, **kwargs: Any) -> DispatchResult:
        """Sends a `block_actions` request. `respond()` calls are recorded in the result."""
        return self.dispatch(payloads.block_action(action_id, **self._with_response_url(kwargs)))

    def shortcut(self, callback_id: str, **kwargs: Any) -> DispatchResult:
        """Sends a global shortcut."""
        return self.dispatch(payloads.shortcut(callback_id, **kwargs))

    def message_shortcut(self, callback_id: str, **kwargs: Any) -> DispatchResult:
        """Sends a message shortcut. `respond()` calls are recorded in the result."""
        return self.dispatch(payloads.message_shortcut(callback_id, **self._with_response_url(kwargs)))

    def view_submission(
        self,
        callback_id: str,
        values: Optional[Dict[str, Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> DispatchResult:
        """Sends a `view_submission` request for a modal."""
        return self.dispatch(payloads.view_submission(callback_id, values, **kwargs))


__all__: Sequence[str] = ["BoltTestClient", "DispatchResult", "InlineExecutor"]
