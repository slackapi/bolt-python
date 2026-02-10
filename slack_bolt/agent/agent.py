from typing import Optional

from slack_sdk import WebClient
from slack_sdk.web.chat_stream import ChatStream


class BoltAgent:
    """Agent listener argument for building AI-powered Slack agents.

    Experimental:
        This API is experimental and may change in future releases.

        @app.event("app_mention")
        def handle_mention(agent):
            stream = agent.chat_stream()
            stream.append(markdown_text="Hello!")
            stream.stop()
    """

    def __init__(
        self,
        *,
        client: WebClient,
        channel_id: Optional[str] = None,
        thread_ts: Optional[str] = None,
        team_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ):
        self._client = client
        self._channel_id = channel_id
        self._thread_ts = thread_ts
        self._team_id = team_id
        self._user_id = user_id

    def chat_stream(
        self,
        *,
        channel: Optional[str] = None,
        thread_ts: Optional[str] = None,
        recipient_team_id: Optional[str] = None,
        recipient_user_id: Optional[str] = None,
        **kwargs,
    ) -> ChatStream:
        """Creates a ChatStream with defaults from event context.

        Each call creates a new instance. Create multiple for parallel streams.

        Args:
            channel: Channel ID. Defaults to the channel from the event context.
            thread_ts: Thread timestamp. Defaults to the thread_ts from the event context.
            recipient_team_id: Team ID of the recipient. Defaults to the team from the event context.
            recipient_user_id: User ID of the recipient. Defaults to the user from the event context.
            **kwargs: Additional arguments passed to ``WebClient.chat_stream()``.

        Returns:
            A new ``ChatStream`` instance.
        """
        resolved_channel = channel or self._channel_id
        resolved_thread_ts = thread_ts or self._thread_ts
        if resolved_channel is None:
            raise ValueError(
                "channel is required: provide it as an argument or ensure channel_id is set in the event context"
            )
        if resolved_thread_ts is None:
            raise ValueError(
                "thread_ts is required: provide it as an argument or ensure thread_ts is set in the event context"
            )
        return self._client.chat_stream(
            channel=resolved_channel,
            thread_ts=resolved_thread_ts,
            recipient_team_id=recipient_team_id or self._team_id,
            recipient_user_id=recipient_user_id or self._user_id,
            **kwargs,
        )
