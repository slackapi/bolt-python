"""Pure helpers shared by the sync and async test clients.

This module is intentionally free of any ``aiohttp`` / ``asyncio`` imports so it
can be safely imported on the sync path (mirroring ``context/*/internals.py``).
It only knows how to (1) turn a payload dict into the exact wire encoding Slack
would send and (2) build signed request headers the way Slack signs its requests.
"""

import json
import time
from enum import Enum
from typing import Any, Dict, Optional, Sequence, Tuple
from urllib.parse import urlencode

from slack_sdk.signature import SignatureVerifier

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_FORM = "application/x-www-form-urlencoded"


class WireFormat(Enum):
    """The three wire encodings Slack uses for inbound requests.

    See ``slack_bolt/request/internals.py::parse_body`` for the receiving side.
    """

    JSON = "json"  # Events API envelope -> application/json
    FORM = "form"  # Slash command -> urlencoded flat form
    PAYLOAD = "payload"  # Interactivity -> payload=<urlencoded json>


def encode_wire_body(wire_format: WireFormat, body: Dict[str, Any]) -> Tuple[str, str]:
    """Return ``(content_type, raw_body)`` for the given wire format.

    - ``WireFormat.JSON``: JSON event envelope (``application/json``).
    - ``WireFormat.FORM``: flat urlencoded form, e.g. a slash command.
    - ``WireFormat.PAYLOAD``: ``payload=<urlencoded json>`` used by every interactivity
      request (actions, shortcuts, views, options).
    """
    if wire_format == WireFormat.JSON:
        return CONTENT_TYPE_JSON, json.dumps(body)
    if wire_format == WireFormat.FORM:
        return CONTENT_TYPE_FORM, urlencode(body)
    if wire_format == WireFormat.PAYLOAD:
        return CONTENT_TYPE_FORM, urlencode({"payload": json.dumps(body)})
    raise ValueError(f"Unknown wire_format: {wire_format}")


def build_signed_headers(
    *,
    signing_secret: str,
    content_type: str,
    raw_body: str,
    timestamp: Optional[str] = None,
) -> Dict[str, Sequence[str]]:
    """Build headers with a valid ``x-slack-signature`` so ``RequestVerification`` passes.

    ``timestamp`` defaults to now because ``SignatureVerifier.is_valid`` rejects
    timestamps more than five minutes old.
    """
    ts = timestamp if timestamp is not None else str(int(time.time()))
    signature = SignatureVerifier(signing_secret).generate_signature(timestamp=ts, body=raw_body)
    return {
        "content-type": [content_type],
        "x-slack-signature": [signature if signature is not None else ""],
        "x-slack-request-timestamp": [ts],
    }


def build_unsigned_headers(content_type: str) -> Dict[str, Sequence[str]]:
    """Headers for the ``verify=False`` (socket_mode) path -- no signature needed."""
    return {"content-type": [content_type]}
