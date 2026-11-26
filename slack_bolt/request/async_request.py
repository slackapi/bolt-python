from typing import Dict, Optional, Union, Any, Sequence

from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.error import BoltError
from slack_bolt.request.internals import (
    parse_query,
    build_normalized_headers,
    extract_content_type,
    error_message_raw_body_required_in_http_mode,
)
from slack_bolt.util.utils import create_copy


class AsyncBoltRequest:
    raw_body: str
    body: Dict[str, Any]
    query: Dict[str, Sequence[str]]
    headers: Dict[str, Sequence[str]]
    content_type: Optional[str]
    context: AsyncBoltContext
    lazy_only: bool
    lazy_function_name: Optional[str]
    mode: str  # either "http" or "socket_mode"

    def __init__(
        self,
        *,
        body: Union[str, dict],
        query: Optional[Union[str, Dict[str, str], Dict[str, Sequence[str]]]] = None,
        headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None,
        context: Optional[Dict[str, Any]] = None,
        mode: str = "http",  # either "http" or "socket_mode"
    ):
        """Request to a Bolt app.

        The body is parsed and the context is built from it when the app dispatches the request,
        right after request verification, so unsigned payloads are never parsed.

        Args:
            body: The raw request body (only plain text is supported for "http" mode)
            query: The query string data in any data format.
            headers: The request headers.
            context: The context in this request.
            mode: The mode used for this request. (either "http" or "socket_mode")
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
        self.context = AsyncBoltContext(context if context else {})
        self.lazy_only = bool(self.headers.get("x-slack-bolt-lazy-only", [False])[0])
        self.lazy_function_name = self.headers.get("x-slack-bolt-lazy-function-name", [None])[0]
        self.mode = mode

    def to_copyable(self) -> "AsyncBoltRequest":
        body: Union[str, dict] = self.raw_body if self.mode == "http" else self.body
        copied = AsyncBoltRequest(
            body=body,
            query=self.query,
            headers=self.headers,
            context=self.context.to_copyable(),
            mode=self.mode,
        )
        copied.body = create_copy(self.body)
        return copied
