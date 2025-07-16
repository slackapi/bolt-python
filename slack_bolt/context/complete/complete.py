from typing import Any, Dict, Optional

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse


class Complete:
    client: WebClient
    function_execution_id: Optional[str]

    def __init__(
        self,
        client: WebClient,
        function_execution_id: Optional[str],
    ):
        self.client = client
        self.function_execution_id = function_execution_id

    def __call__(self, outputs: Optional[Dict[str, Any]] = None) -> SlackResponse:
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

        return self.client.functions_completeSuccess(function_execution_id=self.function_execution_id, outputs=outputs or {})
