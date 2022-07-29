from typing import Optional, Union

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse


class CompleteSuccess:
    client: Optional[WebClient]
    function_execution_id: Optional[str]

    def __init__(
        self,
        client: Optional[WebClient],
        function_execution_id: Optional[str],
    ):
        self.client = client
        self.function_execution_id = function_execution_id

    def __call__(
        self,
        outputs: Union[str, dict],
    ) -> SlackResponse:
        if self._can_complete():
            return self.client.api_call(
                "functions.completeSuccess", json={"outputs": outputs, "function_execution_id": self.function_execution_id}
            )
        else:
            raise ValueError("success is unsupported here as there is no function_execution_id")

    def _can_complete(self) -> bool:
        return hasattr(self, "client") and self.client is not None and self.function_execution_id is not None
