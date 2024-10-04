from logging import Logger
from typing import Any, Dict, Optional, Tuple

from slack_bolt.authorization import AuthorizeResult


class BaseContext(dict):
    """Context object associated with a request from Slack."""

    copyable_standard_property_names = [
        "logger",
        "token",
        "enterprise_id",
        "is_enterprise_install",
        "team_id",
        "user_id",
        "actor_enterprise_id",
        "actor_team_id",
        "actor_user_id",
        "channel_id",
        "thread_ts",
        "response_url",
        "matches",
        "authorize_result",
        "function_bot_access_token",
        "bot_token",
        "bot_id",
        "bot_user_id",
        "user_token",
        "function_execution_id",
        "inputs",
        "client",
        "ack",
        "say",
        "respond",
        "complete",
        "fail",
        "set_status",
        "set_title",
        "set_suggested_prompts",
    ]
    # Note that these items are not copyable, so when you add new items to this list,
    # you must modify ThreadListenerRunner/AsyncioListenerRunner's _build_lazy_request method to pass the values.
    # Other listener runners do not require the change because they invoke a lazy listener over the network,
    # meaning that the context initialization would be done again.
    non_copyable_standard_property_names = [
        "listener_runner",
        "get_thread_context",
        "save_thread_context",
    ]

    standard_property_names = copyable_standard_property_names + non_copyable_standard_property_names

    @property
    def logger(self) -> Logger:
        """The properly configured logger that is available for middleware/listeners."""
        return self["logger"]

    @property
    def token(self) -> Optional[str]:
        """The (bot/user) token resolved for this request."""
        return self.get("token")

    @property
    def enterprise_id(self) -> Optional[str]:
        """The Enterprise Grid Organization ID of this request."""
        return self.get("enterprise_id")

    @property
    def is_enterprise_install(self) -> Optional[bool]:
        """True if the request is associated with an Org-wide installation."""
        return self.get("is_enterprise_install")

    @property
    def team_id(self) -> Optional[str]:
        """The Workspace ID of this request."""
        return self.get("team_id")

    @property
    def user_id(self) -> Optional[str]:
        """The user ID associated ith this request."""
        return self.get("user_id")

    @property
    def actor_enterprise_id(self) -> Optional[str]:
        """The action's actor's Enterprise Grid organization ID.
        Note that this property is especially useful for handling events in Slack Connect channels.
        That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.
        """
        return self.get("actor_enterprise_id")

    @property
    def actor_team_id(self) -> Optional[str]:
        """The action's actor's workspace ID.
        Note that this property is especially useful for handling events in Slack Connect channels.
        That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.
        """
        return self.get("actor_team_id")

    @property
    def actor_user_id(self) -> Optional[str]:
        """The action's actor's user ID.
        Note that this property is especially useful for handling events in Slack Connect channels.
        That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.
        """
        return self.get("actor_user_id")

    @property
    def channel_id(self) -> Optional[str]:
        """The conversation ID associated with this request."""
        return self.get("channel_id")

    @property
    def thread_ts(self) -> Optional[str]:
        """The conversation thread's ID associated with this request."""
        return self.get("thread_ts")

    @property
    def response_url(self) -> Optional[str]:
        """The `response_url` associated with this request."""
        return self.get("response_url")

    @property
    def matches(self) -> Optional[Tuple]:
        """Returns all the matched parts in message listener's regexp"""
        return self.get("matches")

    @property
    def function_execution_id(self) -> Optional[str]:
        """The `function_execution_id` associated with this request.
        Only available for `function_executed` and interactivity events scoped to a custom step.
        """
        return self.get("function_execution_id")

    @property
    def inputs(self) -> Optional[Dict[str, Any]]:
        """The `inputs` associated with this request.
        Only available for `function_executed` and interactivity events scoped to a custom step.
        """
        return self.get("inputs")

    # --------------------------------

    @property
    def authorize_result(self) -> Optional[AuthorizeResult]:
        """The authorize result resolved for this request."""
        return self.get("authorize_result")

    @property
    def function_bot_access_token(self) -> Optional[str]:
        """The bot token resolved for this function request.
        Only available for `function_executed` and interactivity events scoped to a custom step.
        """
        return self.get("function_bot_access_token")

    @property
    def bot_token(self) -> Optional[str]:
        """The bot token resolved for this request."""
        return self.get("bot_token")

    @property
    def bot_id(self) -> Optional[str]:
        """The bot ID resolved for this request."""
        return self.get("bot_id")

    @property
    def bot_user_id(self) -> Optional[str]:
        """The bot user ID resolved for this request."""
        return self.get("bot_user_id")

    @property
    def user_token(self) -> Optional[str]:
        """The user token resolved for this request."""
        return self.get("user_token")

    def set_authorize_result(self, authorize_result: AuthorizeResult):
        self["authorize_result"] = authorize_result
        if authorize_result.bot_id is not None:
            self["bot_id"] = authorize_result.bot_id
        if authorize_result.bot_user_id is not None:
            self["bot_user_id"] = authorize_result.bot_user_id
        if authorize_result.bot_token is not None:
            self["bot_token"] = authorize_result.bot_token
        if authorize_result.user_id is not None:
            self["user_id"] = authorize_result.user_id
        if authorize_result.user_token is not None:
            self["user_token"] = authorize_result.user_token
