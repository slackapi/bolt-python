from typing import Dict, Optional, Union, Any, Sequence

from slack_bolt.context.context import BoltContext
from slack_bolt.error import BoltError
from slack_bolt.request.internals import (
    parse_query,
    parse_body,
    build_normalized_headers,
    build_context,
    extract_content_type,
    error_message_raw_body_required_in_http_mode,
)


class BoltRequest:
    raw_body: str
    query: Dict[str, Sequence[str]]
    headers: Dict[str, Sequence[str]]
    content_type: Optional[str]
    body: Dict[str, Any]
    context: BoltContext
    lazy_only: bool
    lazy_function_name: Optional[str]
    mode: str  # either "http" or "socket_mode"
    defer_parsing: bool

    def __init__(
        self,
        *,
        body: Union[str, dict],
        query: Optional[Union[str, Dict[str, str], Dict[str, Sequence[str]]]] = None,
        headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None,
        context: Optional[Dict[str, Any]] = None,
        mode: str = "http",  # either "http" or "socket_mode"
        defer_parsing: bool = False,
    ):
        """Request to a Bolt app.

        Args:
            body: The raw request body (only plain text is supported for "http" mode)
            query: The query string data in any data format.
            headers: The request headers.
            context: The context in this request.
            mode: The mode used for this request. (either "http" or "socket_mode")
            defer_parsing: True to leave `body` empty and skip building `context` from it until
                the built-in `RequestParsing` middleware runs after `RequestVerification`.
                Adapters set this so unsigned payloads are never parsed.
        """
        if mode == "http":
            # HTTP Mode
            if body is not None and not isinstance(body, str):
                raise BoltError(error_message_raw_body_required_in_http_mode())
            self.raw_body = body if body is not None else ""
        else:
            # Socket Mode
            if body is not None and isinstance(body, str):
                self.raw_body = body
            else:
                # We don't convert the dict value to str
                # as doing so does not guarantee to keep the original structure/format.
                self.raw_body = ""

        self.query = parse_query(query)
        self.headers = build_normalized_headers(headers)
        self.content_type = extract_content_type(self.headers)

        self.body = body if isinstance(body, dict) else {}
        self.context = BoltContext(context if context else {})
        self.defer_parsing = defer_parsing
        if not defer_parsing:
            self._parse_body_and_build_context()
        self.lazy_only = bool(self.headers.get("x-slack-bolt-lazy-only", [False])[0])
        self.lazy_function_name = self.headers.get("x-slack-bolt-lazy-function-name", [None])[0]
        self.mode = mode

    def complete_deferred_parsing(self) -> None:
        """Parses the body and builds the context of a request created with `defer_parsing=True`.

        Context values set after the request was created take precedence over the ones in the body.
        """
        if not self.defer_parsing:
            return
        set_after_creation = dict(self.context)
        self._parse_body_and_build_context()
        self.context.update(set_after_creation)
        self.defer_parsing = False

    def _parse_body_and_build_context(self) -> None:
        if self.raw_body:
            self.body = parse_body(self.raw_body, self.content_type)
        build_context(self.context, self.body)

    def to_copyable(self) -> "BoltRequest":
        body: Union[str, dict] = self.raw_body if self.mode == "http" else self.body
        return BoltRequest(
            body=body,
            query=self.query,
            headers=self.headers,
            context=self.context.to_copyable(),
            mode=self.mode,
        )
