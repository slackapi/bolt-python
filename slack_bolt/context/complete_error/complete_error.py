from typing import Optional

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse


class CompleteError:
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
        message: str,
    ) -> SlackResponse:
        if self._can_complete():
            if isinstance(message, str):
                # TODO add this new api call to the sdk and use it here
                return self.client.api_call(
                    "functions.completeError", json={"error": message, "function_execution_id": self.function_execution_id}
                )
            raise ValueError(f"The message arg is unexpected type ({type(message)}) expecting str")
        else:
            raise ValueError("complete_error is unsupported here as there is no function_execution_id")

    def _can_complete(self) -> bool:
        return hasattr(self, "client") and self.client is not None and self.function_execution_id is not None
