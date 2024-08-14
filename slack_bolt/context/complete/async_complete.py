from typing import Any, Dict, Optional

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse


class AsyncComplete:
    client: AsyncWebClient
    function_execution_id: Optional[str]

    def __init__(
        self,
        client: AsyncWebClient,
        function_execution_id: Optional[str],
    ):
        self.client = client
        self.function_execution_id = function_execution_id

    async def __call__(self, outputs: Optional[Dict[str, Any]] = None) -> AsyncSlackResponse:
        """Signal the successful completion of the custom function.

        Kwargs:
            outputs: Json serializable object containing the output values

        Returns:
            SlackResponse: The response object returned from slack

        Raises:
            ValueError: If this function cannot be used.
        """
        if self.function_execution_id is None:
            raise ValueError("complete is unsupported here as there is no function_execution_id")

        return await self.client.functions_completeSuccess(
            function_execution_id=self.function_execution_id, outputs=outputs or {}
        )
