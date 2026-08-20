"""Request factory and typed request dataclasses.

This module is pure data -- it builds the Python ``dict`` payloads Slack would
send for each handler type. It imports neither ``aiohttp`` nor ``asyncio``, so it
is shared unchanged by both :class:`SlackTestClient` and
:class:`AsyncSlackTestClient` (mirroring how ``context/*/internals.py`` is shared
by the sync and async context utilities).

Two usage styles are supported:

- **Factory** -- :class:`SlackRequestFactory` holds suite-level defaults (team_id,
  user_id, ...) and has one method per handler type. Per-call keyword arguments
  override the factory defaults for that one request.
- **Direct** -- every request dataclass (:class:`CommandRequest`,
  :class:`EventRequest`, ...) is directly constructable with all fields defaulted,
  for one-off requests that do not want shared state.

The wire encoding each request uses is declared by its ``wire_format`` class
attribute (a :class:`~slack_bolt.testing.internals.WireFormat` member) and consumed
by ``internals.encode_wire_body``.
"""

import dataclasses
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional, Type, TypeVar, Union

from .internals import WireFormat

# Dummy identity defaults (never real values -- see AGENTS.md test guidance).
DEFAULT_TEAM_ID = "T111"
DEFAULT_USER_ID = "W111"
DEFAULT_CHANNEL_ID = "C111"
DEFAULT_API_APP_ID = "A111"
DEFAULT_TRIGGER_ID = "111.111.xxxxxxxxxxxxxxxxxxxxxxxx"
DEFAULT_RESPONSE_URL = "https://hooks.slack.com/actions/T111/111111/xxxxxxxxxxxxxxxxxxxx"
DEFAULT_VERIFICATION_TOKEN = "verification-token"
DEFAULT_TS = "1599616881.000100"


@dataclass
class SlackTestRequest:
    """Base for every request dataclass: the identity fields common to all payloads."""

    team_id: str = DEFAULT_TEAM_ID
    enterprise_id: Optional[str] = None
    user_id: str = DEFAULT_USER_ID
    channel_id: str = DEFAULT_CHANNEL_ID
    api_app_id: str = DEFAULT_API_APP_ID
    is_enterprise_install: bool = False
    token: str = DEFAULT_VERIFICATION_TOKEN

    #: The wire encoding for this request; one of the :class:`WireFormat` members.
    wire_format: ClassVar[WireFormat] = WireFormat.JSON

    def build_body(self) -> Dict[str, Any]:
        """Return the parsed payload dict this request represents."""
        raise NotImplementedError

    # -- shared payload fragments --

    def _team(self) -> Dict[str, Any]:
        return {"id": self.team_id, "domain": "example"}

    def _enterprise(self) -> Optional[Dict[str, Any]]:
        return {"id": self.enterprise_id, "name": "Example Org"} if self.enterprise_id else None

    def _user(self) -> Dict[str, Any]:
        return {"id": self.user_id, "username": "user", "team_id": self.team_id}

    def _authorizations(self) -> List[Dict[str, Any]]:
        return [
            {
                "enterprise_id": self.enterprise_id,
                "team_id": self.team_id,
                "user_id": self.user_id,
                "is_bot": True,
                "is_enterprise_install": self.is_enterprise_install,
            }
        ]


@dataclass
class CommandRequest(SlackTestRequest):
    command: str = "/hello"
    text: str = ""
    response_url: str = DEFAULT_RESPONSE_URL
    trigger_id: str = DEFAULT_TRIGGER_ID

    wire_format: ClassVar[WireFormat] = WireFormat.FORM

    def build_body(self) -> Dict[str, Any]:
        body = {
            "token": self.token,
            "team_id": self.team_id,
            "team_domain": "example",
            "channel_id": self.channel_id,
            "channel_name": "general",
            "user_id": self.user_id,
            "user_name": "user",
            "command": self.command,
            "text": self.text,
            "api_app_id": self.api_app_id,
            "response_url": self.response_url,
            "trigger_id": self.trigger_id,
        }
        if self.enterprise_id:
            body["enterprise_id"] = self.enterprise_id
            body["enterprise_name"] = "Example Org"
        return body


@dataclass
class EventRequest(SlackTestRequest):
    event: Dict[str, Any] = field(default_factory=lambda: {"type": "app_mention", "text": "<@UB111> hi"})
    event_id: str = "Ev111"
    event_time: int = 1599616881

    wire_format: ClassVar[WireFormat] = WireFormat.JSON

    def build_body(self) -> Dict[str, Any]:
        event = dict(self.event)
        event.setdefault("user", self.user_id)
        event.setdefault("channel", self.channel_id)
        event.setdefault("ts", DEFAULT_TS)
        event.setdefault("event_ts", DEFAULT_TS)
        body: Dict[str, Any] = {
            "token": self.token,
            "team_id": self.team_id,
            "api_app_id": self.api_app_id,
            "event": event,
            "type": "event_callback",
            "event_id": self.event_id,
            "event_time": self.event_time,
            "authorizations": self._authorizations(),
            "is_ext_shared_channel": False,
        }
        if self.enterprise_id:
            body["enterprise_id"] = self.enterprise_id
        return body


@dataclass
class ActionRequest(SlackTestRequest):
    action_id: str = "button"
    block_id: str = "block"
    value: Optional[str] = "click_me"
    action_type: str = "button"
    response_url: str = DEFAULT_RESPONSE_URL
    trigger_id: str = DEFAULT_TRIGGER_ID

    wire_format: ClassVar[WireFormat] = WireFormat.PAYLOAD

    def build_body(self) -> Dict[str, Any]:
        action: Dict[str, Any] = {
            "type": self.action_type,
            "action_id": self.action_id,
            "block_id": self.block_id,
            "action_ts": "1599616881.000000",
        }
        if self.value is not None:
            action["value"] = self.value
        return {
            "type": "block_actions",
            "user": self._user(),
            "api_app_id": self.api_app_id,
            "token": self.token,
            "container": {"type": "message", "message_ts": DEFAULT_TS},
            "trigger_id": self.trigger_id,
            "team": self._team(),
            "enterprise": self._enterprise(),
            "is_enterprise_install": self.is_enterprise_install,
            "channel": {"id": self.channel_id, "name": "general"},
            "response_url": self.response_url,
            "actions": [action],
        }


@dataclass
class ShortcutRequest(SlackTestRequest):
    callback_id: str = "test-shortcut"
    trigger_id: str = DEFAULT_TRIGGER_ID

    wire_format: ClassVar[WireFormat] = WireFormat.PAYLOAD

    def build_body(self) -> Dict[str, Any]:
        return {
            "type": "shortcut",
            "token": self.token,
            "action_ts": "1599616881.000000",
            "team": self._team(),
            "enterprise": self._enterprise(),
            "is_enterprise_install": self.is_enterprise_install,
            "user": self._user(),
            "callback_id": self.callback_id,
            "trigger_id": self.trigger_id,
        }


@dataclass
class ViewSubmissionRequest(SlackTestRequest):
    callback_id: str = "test-view"
    state_values: Dict[str, Any] = field(default_factory=dict)
    view_id: str = "V111"
    trigger_id: str = DEFAULT_TRIGGER_ID

    wire_format: ClassVar[WireFormat] = WireFormat.PAYLOAD

    def _view(self) -> Dict[str, Any]:
        return {
            "id": self.view_id,
            "type": "modal",
            "callback_id": self.callback_id,
            "team_id": self.team_id,
            "state": {"values": self.state_values},
            "hash": "111.abc",
            "title": {"type": "plain_text", "text": "Test"},
            "blocks": [],
            "private_metadata": "",
        }

    def build_body(self) -> Dict[str, Any]:
        return {
            "type": "view_submission",
            "token": self.token,
            "team": self._team(),
            "enterprise": self._enterprise(),
            "is_enterprise_install": self.is_enterprise_install,
            "user": self._user(),
            "api_app_id": self.api_app_id,
            "trigger_id": self.trigger_id,
            "view": self._view(),
        }


@dataclass
class ViewClosedRequest(ViewSubmissionRequest):
    is_cleared: bool = False

    wire_format: ClassVar[WireFormat] = WireFormat.PAYLOAD

    def build_body(self) -> Dict[str, Any]:
        body = super().build_body()
        body["type"] = "view_closed"
        body["is_cleared"] = self.is_cleared
        del body["trigger_id"]  # view_closed payloads carry no trigger_id
        return body


@dataclass
class OptionsRequest(SlackTestRequest):
    action_id: str = "select"
    block_id: str = "block"
    value: str = ""

    wire_format: ClassVar[WireFormat] = WireFormat.PAYLOAD

    def build_body(self) -> Dict[str, Any]:
        return {
            "type": "block_suggestion",
            "token": self.token,
            "action_id": self.action_id,
            "block_id": self.block_id,
            "value": self.value,
            "team": self._team(),
            "enterprise": self._enterprise(),
            "is_enterprise_install": self.is_enterprise_install,
            "user": self._user(),
            "api_app_id": self.api_app_id,
            "container": {"type": "view", "view_id": "V111"},
        }


@dataclass
class FunctionRequest(SlackTestRequest):
    callback_id: str = "test-function"
    function_execution_id: str = "Fx111"
    inputs: Dict[str, Any] = field(default_factory=dict)
    bot_access_token: str = "xwfp-valid"
    event_id: str = "Ev111"
    event_time: int = 1599616881

    wire_format: ClassVar[WireFormat] = WireFormat.JSON

    def build_body(self) -> Dict[str, Any]:
        event = {
            "type": "function_executed",
            "function": {"id": "Fn111", "callback_id": self.callback_id},
            "inputs": self.inputs,
            "function_execution_id": self.function_execution_id,
            "bot_access_token": self.bot_access_token,
            "event_ts": DEFAULT_TS,
        }
        body: Dict[str, Any] = {
            "token": self.token,
            "team_id": self.team_id,
            "api_app_id": self.api_app_id,
            "event": event,
            "type": "event_callback",
            "event_id": self.event_id,
            "event_time": self.event_time,
            "authorizations": self._authorizations(),
        }
        if self.enterprise_id:
            body["enterprise_id"] = self.enterprise_id
        return body


T = TypeVar("T", bound=SlackTestRequest)


class SlackRequestFactory:
    """Builds request dataclasses, applying suite-level defaults.

    Example::

        f = SlackRequestFactory(team_id="T1", user_id="U1")
        f.command("/hi", text="world")          # CommandRequest with those defaults
        f.command("/hi", user_id="U999")        # per-call override beats the default
    """

    def __init__(self, **defaults: Any) -> None:
        self.defaults = defaults

    def _make(self, cls: Type[T], **overrides: Any) -> T:
        valid = {f.name for f in dataclasses.fields(cls)}
        params: Dict[str, Any] = {k: v for k, v in self.defaults.items() if k in valid}
        params.update(overrides)
        return cls(**params)

    def command(self, command: str = "/hello", **kwargs: Any) -> CommandRequest:
        return self._make(CommandRequest, command=command, **kwargs)

    def event(self, event: Union[str, Dict[str, Any]], **kwargs: Any) -> EventRequest:
        ev = {"type": event} if isinstance(event, str) else dict(event)
        return self._make(EventRequest, event=ev, **kwargs)

    def message(self, text: str = "hello", channel_type: str = "channel", **kwargs: Any) -> EventRequest:
        event = {"type": "message", "text": text, "channel_type": channel_type}
        return self._make(EventRequest, event=event, **kwargs)

    def action(self, action_id: str = "button", **kwargs: Any) -> ActionRequest:
        return self._make(ActionRequest, action_id=action_id, **kwargs)

    def shortcut(self, callback_id: str = "test-shortcut", **kwargs: Any) -> ShortcutRequest:
        return self._make(ShortcutRequest, callback_id=callback_id, **kwargs)

    def view_submission(self, callback_id: str = "test-view", **kwargs: Any) -> ViewSubmissionRequest:
        return self._make(ViewSubmissionRequest, callback_id=callback_id, **kwargs)

    def view_closed(self, callback_id: str = "test-view", **kwargs: Any) -> ViewClosedRequest:
        return self._make(ViewClosedRequest, callback_id=callback_id, **kwargs)

    def options(self, action_id: str = "select", **kwargs: Any) -> OptionsRequest:
        return self._make(OptionsRequest, action_id=action_id, **kwargs)

    def function(self, callback_id: str = "test-function", **kwargs: Any) -> FunctionRequest:
        return self._make(FunctionRequest, callback_id=callback_id, **kwargs)
