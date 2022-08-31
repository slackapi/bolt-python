from typing import Optional

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse
from slack_bolt.context.complete_error.internals import _can_complete


class AsyncCompleteError:
    client: Optional[AsyncWebClient]
    function_execution_id: Optional[str]

    def __init__(
        self,
        client: Optional[AsyncWebClient],
        function_execution_id: Optional[str],
    ):
        self.client = client
        self.function_execution_id = function_execution_id

    async def __call__(
        self,
        message: str,
    ) -> AsyncSlackResponse:
        if _can_complete(self):
            if isinstance(message, str):
                # TODO add this new api call to the sdk and use it here
                return await self.client.api_call(
                    "functions.completeError", json={"error": message, "function_execution_id": self.function_execution_id}
                )
            raise ValueError(f"The message arg is unexpected type ({type(message)}) expecting str")
        else:
            raise ValueError("complete_error is unsupported here as there is no function_execution_id")
