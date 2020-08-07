from typing import Dict, Optional, List, Union, Any

from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.request.async_internals import build_async_context
from slack_bolt.request.internals import (
    parse_query,
    parse_payload,
    build_normalized_headers,
    extract_content_type,
)


class AsyncBoltRequest:
    body: str
    query: Dict[str, List[str]]
    headers: Dict[str, List[str]]
    content_type: Optional[str]
    payload: Dict[str, Any]
    context: AsyncBoltContext
    lazy_only: bool
    lazy_function_name: Optional[str]

    def __init__(
        self,
        *,
        body: str,
        query: Optional[Union[str, Dict[str, str], Dict[str, List[str]]]] = None,
        # many framework use Dict[str, str] but the reality is Dict[str, List[str]]
        headers: Optional[Dict[str, Union[str, List[str]]]] = None,
        context: Optional[Dict[str, str]] = None,
    ):
        self.body = body
        self.query = parse_query(query)
        self.headers = build_normalized_headers(headers)
        self.content_type = extract_content_type(self.headers)
        self.payload = parse_payload(self.body, self.content_type)
        self.context = build_async_context(
            AsyncBoltContext(context if context else {}), self.payload
        )
        self.lazy_only = self.headers.get("x-slack-bolt-lazy-only", [False])[0]
        self.lazy_function_name = self.headers.get(
            "x-slack-bolt-lazy-function-name", [None]
        )[0]
