from typing import Optional

from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.context.agent.tool_registry import AgentToolRegistry


class AsyncAgentUtilities:
    """Experimental: Per-request async agent utilities injected as the ``agent`` listener argument.

    Provides access to the tool registry and convenience methods for building
    AI-powered Slack agents in async apps.

    Attributes:
        tools: Per-request tool registry (copy of the global registry). Adding tools
            here does not affect other requests.
    """

    client: AsyncWebClient
    channel_id: Optional[str]
    thread_ts: Optional[str]
    team_id: Optional[str]
    user_id: Optional[str]
    tools: AgentToolRegistry

    def __init__(
        self,
        *,
        client: AsyncWebClient,
        channel_id: Optional[str] = None,
        thread_ts: Optional[str] = None,
        team_id: Optional[str] = None,
        user_id: Optional[str] = None,
        tool_registry: Optional[AgentToolRegistry] = None,
    ):
        self.client = client
        self.channel_id = channel_id
        self.thread_ts = thread_ts
        self.team_id = team_id
        self.user_id = user_id
        self.tools = tool_registry or AgentToolRegistry()

    def chat_stream(
        self,
        *,
        channel: Optional[str] = None,
        thread_ts: Optional[str] = None,
        recipient_team_id: Optional[str] = None,
        recipient_user_id: Optional[str] = None,
        **kwargs,
    ):
        """Create a new chat stream with context defaults pre-filled.

        Wraps ``AsyncWebClient.chat_stream()`` with sensible defaults from the
        current event context. Each call creates a fresh stream instance.

        Args:
            channel: Target channel ID. Defaults to the event's channel.
            thread_ts: Thread timestamp. Defaults to the event's thread.
            recipient_team_id: Target team ID. Defaults to the event's team.
            recipient_user_id: Target user ID. Defaults to the event's user.
            **kwargs: Additional keyword arguments passed to ``client.chat_stream()``.

        Returns:
            A chat stream instance from the Slack SDK.
        """
        return self.client.chat_stream(
            channel=channel or self.channel_id,
            thread_ts=thread_ts or self.thread_ts,
            recipient_team_id=recipient_team_id or self.team_id,
            recipient_user_id=recipient_user_id or self.user_id,
            **kwargs,
        )
