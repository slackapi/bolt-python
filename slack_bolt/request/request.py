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
    error_message_unknown_request_body_type,
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

    def __init__(
        self,
        *,
        body: Union[str, dict],
        query: Optional[Union[str, Dict[str, str], Dict[str, Sequence[str]]]] = None,
        headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None,
        context: Optional[Dict[str, str]] = None,
        mode: str = "http",  # either "http" or "socket_mode"
    ):
        """Request to a Bolt app.

        :param body: The raw request body (only plain text is supported for "http" mode)
        :param query: The query string data in any data format.
        :param headers: The request headers.
        :param context: The context in this request.
        :param mode: The mode used for this request. (either "http" or "socket_mode")
        """
        if mode == "http" and not isinstance(body, str):
            raise BoltError(error_message_raw_body_required_in_http_mode())
        self.raw_body = body if mode == "http" else ""
        self.query = parse_query(query)
        self.headers = build_normalized_headers(headers)
        self.content_type = extract_content_type(self.headers)
        if isinstance(body, str):
            self.body = parse_body(self.raw_body, self.content_type)
        elif isinstance(body, dict):
            self.body = body
        else:
            raise BoltError(error_message_unknown_request_body_type())

        self.context = build_context(BoltContext(context if context else {}), self.body)
        self.lazy_only = self.headers.get("x-slack-bolt-lazy-only", [False])[0]
        self.lazy_function_name = self.headers.get(
            "x-slack-bolt-lazy-function-name", [None]
        )[0]
        self.mode = mode
