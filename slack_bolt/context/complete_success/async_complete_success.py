from typing import Optional, Union

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse
from slack_bolt.context.complete_success.internals import _can_complete


class AsyncCompleteSuccess:
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
        outputs: Union[str, dict],
    ) -> AsyncSlackResponse:
        if _can_complete(self):
            if isinstance(outputs, dict) or isinstance(outputs, str):
                # TODO add this new api call to the sdk and use it here
                return await self.client.api_call(
                    "functions.completeSuccess",
                    json={"outputs": outputs, "function_execution_id": self.function_execution_id},
                )
            raise ValueError(f"The outputs arg is unexpected type ({type(outputs)}) expecting dict or str")
        else:
            raise ValueError("complete_success is unsupported here as there is no function_execution_id")
