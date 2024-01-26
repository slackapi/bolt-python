from typing import Optional

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse


class AsyncFail:
    client: AsyncWebClient
    function_execution_id: Optional[str]

    def __init__(
        self,
        client: AsyncWebClient,
        function_execution_id: Optional[str],
    ):
        self.client = client
        self.function_execution_id = function_execution_id

    async def __call__(self, error: str) -> AsyncSlackResponse:
        """Signal that the custom function failed to complete.

        Kwargs:
            error: Error message to return to slack

        Returns:
            SlackResponse: The response object returned from slack

        Raises:
            ValueError: If this function cannot be used.
        """
        if self.function_execution_id is None:
            raise ValueError("fail is unsupported here as there is no function_execution_id")

        return await self.client.functions_completeError(function_execution_id=self.function_execution_id, error=error)
