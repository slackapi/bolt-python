"""Utilities for parsing Slack references in message text."""

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

USER_REFERENCE = "user"
CHANNEL_REFERENCE = "channel"
USERGROUP_REFERENCE = "usergroup"
SPECIAL_MENTION_REFERENCE = "special_mention"
DATE_REFERENCE = "date"
LINK_REFERENCE = "link"
UNKNOWN_REFERENCE = "unknown"

_ANGLE_BRACKET_REFERENCE_PATTERN = re.compile(r"<([^<>\n]+)>")
_SPECIAL_MENTION_NAMES = {"here", "channel", "everyone"}

__all__ = [
    "CHANNEL_REFERENCE",
    "DATE_REFERENCE",
    "LINK_REFERENCE",
    "SPECIAL_MENTION_REFERENCE",
    "UNKNOWN_REFERENCE",
    "USER_REFERENCE",
    "USERGROUP_REFERENCE",
    "SlackMessageReference",
    "extract_channel_ids",
    "extract_user_ids",
    "extract_usergroup_ids",
    "parse_slack_references",
]


@dataclass(frozen=True)
class SlackMessageReference:
    """A Slack mrkdwn reference found inside a message text string."""

    type: str
    raw: str
    start: int
    end: int
    id: Optional[str] = None
    label: Optional[str] = None
    url: Optional[str] = None
    special_mention: Optional[str] = None
    timestamp: Optional[str] = None
    date_format: Optional[str] = None
    fallback: Optional[str] = None


def parse_slack_references(text: str) -> List[SlackMessageReference]:
    """Parses Slack mrkdwn references such as user mentions, channel links, and URLs.

    This helper only parses the syntax present in the text. It does not resolve
    IDs to their latest names; use the Slack Web API for current entity data.
    """
    return [_to_slack_message_reference(match) for match in _ANGLE_BRACKET_REFERENCE_PATTERN.finditer(text)]


def extract_user_ids(text: str) -> List[str]:
    return [ref.id for ref in parse_slack_references(text) if ref.type == USER_REFERENCE and ref.id is not None]


def extract_channel_ids(text: str) -> List[str]:
    return [ref.id for ref in parse_slack_references(text) if ref.type == CHANNEL_REFERENCE and ref.id is not None]


def extract_usergroup_ids(text: str) -> List[str]:
    return [ref.id for ref in parse_slack_references(text) if ref.type == USERGROUP_REFERENCE and ref.id is not None]


def _to_slack_message_reference(match: re.Match) -> SlackMessageReference:
    raw = match.group(0)
    inner = match.group(1)
    start, end = match.span()
    target, label = _split_label(inner)

    if target.startswith("@"):
        return _to_user_reference(target=target, label=label, raw=raw, start=start, end=end)

    if target.startswith("#"):
        return _to_channel_reference(target=target, label=label, raw=raw, start=start, end=end)

    if target.startswith("!subteam^"):
        return _to_usergroup_reference(target=target, label=label, raw=raw, start=start, end=end)

    if target.startswith("!date^"):
        return _to_date_reference(target=target, fallback=label, raw=raw, start=start, end=end)

    if target.startswith("!"):
        return _to_special_mention_reference(target=target, label=label, raw=raw, start=start, end=end)

    return SlackMessageReference(type=LINK_REFERENCE, raw=raw, start=start, end=end, url=target, label=label)


def _to_user_reference(
    *,
    target: str,
    label: Optional[str],
    raw: str,
    start: int,
    end: int,
) -> SlackMessageReference:
    user_id = target[1:]
    if not user_id.startswith(("U", "W")):
        return SlackMessageReference(type=UNKNOWN_REFERENCE, raw=raw, start=start, end=end, label=label)
    return SlackMessageReference(type=USER_REFERENCE, raw=raw, start=start, end=end, id=user_id, label=label)


def _to_channel_reference(
    *,
    target: str,
    label: Optional[str],
    raw: str,
    start: int,
    end: int,
) -> SlackMessageReference:
    channel_id = target[1:]
    if channel_id == "":
        return SlackMessageReference(type=UNKNOWN_REFERENCE, raw=raw, start=start, end=end, label=label)
    return SlackMessageReference(type=CHANNEL_REFERENCE, raw=raw, start=start, end=end, id=channel_id, label=label)


def _to_usergroup_reference(
    *,
    target: str,
    label: Optional[str],
    raw: str,
    start: int,
    end: int,
) -> SlackMessageReference:
    prefix_length = len("!subteam^")
    usergroup_id = target[prefix_length:]
    if usergroup_id == "":
        return SlackMessageReference(type=UNKNOWN_REFERENCE, raw=raw, start=start, end=end, label=label)
    return SlackMessageReference(type=USERGROUP_REFERENCE, raw=raw, start=start, end=end, id=usergroup_id, label=label)


def _to_special_mention_reference(
    *,
    target: str,
    label: Optional[str],
    raw: str,
    start: int,
    end: int,
) -> SlackMessageReference:
    name = target[1:]
    if name not in _SPECIAL_MENTION_NAMES:
        return SlackMessageReference(type=UNKNOWN_REFERENCE, raw=raw, start=start, end=end, label=label)
    return SlackMessageReference(
        type=SPECIAL_MENTION_REFERENCE,
        raw=raw,
        start=start,
        end=end,
        label=label,
        special_mention=name,
    )


def _to_date_reference(
    *,
    target: str,
    fallback: Optional[str],
    raw: str,
    start: int,
    end: int,
) -> SlackMessageReference:
    elements = target.split("^", 3)
    if len(elements) < 3 or elements[1] == "" or elements[2] == "":
        return SlackMessageReference(type=UNKNOWN_REFERENCE, raw=raw, start=start, end=end, fallback=fallback)

    url = elements[3] if len(elements) > 3 and elements[3] != "" else None
    return SlackMessageReference(
        type=DATE_REFERENCE,
        raw=raw,
        start=start,
        end=end,
        timestamp=elements[1],
        date_format=elements[2],
        url=url,
        fallback=fallback,
    )


def _split_label(value: str) -> Tuple[str, Optional[str]]:
    if "|" in value:
        target, label = value.split("|", 1)
        return target, label
    return value, None
