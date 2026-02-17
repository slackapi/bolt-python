from typing import List, Optional

from slack_sdk.web.async_client import AsyncSlackResponse, AsyncWebClient
from slack_sdk.web.async_chat_stream import AsyncChatStream


class AsyncBoltAgent:
    """Async agent listener argument for building AI-powered Slack agents.

    Experimental:
        This API is experimental and may change in future releases.

        @app.event("app_mention")
        async def handle_mention(agent):
            stream = await agent.chat_stream()
            await stream.append(markdown_text="Hello!")
            await stream.stop()
    """

    def __init__(
        self,
        *,
        client: AsyncWebClient,
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

    async def chat_stream(
        self,
        *,
        channel: Optional[str] = None,
        thread_ts: Optional[str] = None,
        recipient_team_id: Optional[str] = None,
        recipient_user_id: Optional[str] = None,
        **kwargs,
    ) -> AsyncChatStream:
        """Creates an AsyncChatStream with defaults from event context.

        Each call creates a new instance. Create multiple for parallel streams.

        Args:
            channel: Channel ID. Defaults to the channel from the event context.
            thread_ts: Thread timestamp. Defaults to the thread_ts from the event context.
            recipient_team_id: Team ID of the recipient. Defaults to the team from the event context.
            recipient_user_id: User ID of the recipient. Defaults to the user from the event context.
            **kwargs: Additional arguments passed to ``AsyncWebClient.chat_stream()``.

        Returns:
            A new ``AsyncChatStream`` instance.
        """
        provided = [arg for arg in (channel, thread_ts, recipient_team_id, recipient_user_id) if arg is not None]
        if provided and len(provided) < 4:
            raise ValueError(
                "Either provide all of channel, thread_ts, recipient_team_id, and recipient_user_id, or none of them"
            )
        # Argument validation is delegated to chat_stream() and the API
        return await self._client.chat_stream(
            channel=channel or self._channel_id,  # type: ignore[arg-type]
            thread_ts=thread_ts or self._thread_ts,  # type: ignore[arg-type]
            recipient_team_id=recipient_team_id or self._team_id,
            recipient_user_id=recipient_user_id or self._user_id,
            **kwargs,
        )

    async def set_status(
        self,
        *,
        status: str,
        loading_messages: Optional[List[str]] = None,
        channel: Optional[str] = None,
        thread_ts: Optional[str] = None,
        **kwargs,
    ) -> SlackResponse:
        """Sets the status of an assistant thread.

        Args:
            status: The status text to display.
            loading_messages: Optional list of loading messages to cycle through.
            channel: Channel ID. Defaults to the channel from the event context.
            thread_ts: Thread timestamp. Defaults to the thread_ts from the event context.
            **kwargs: Additional arguments passed to ``AsyncWebClient.assistant_threads_setStatus()``.

        Returns:
            ``SlackResponse`` from the API call.
        """
        return await self._client.assistant_threads_setStatus(
            channel_id=channel or self._channel_id,  # type: ignore[arg-type]
            thread_ts=thread_ts or self._thread_ts,  # type: ignore[arg-type]
            status=status,
            loading_messages=loading_messages,
            **kwargs,
        )
