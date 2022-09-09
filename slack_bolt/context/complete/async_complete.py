from typing import Optional, Union

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse
from slack_bolt.context.complete.internals import get_kwargs_for_logging, get_name_for_logging


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

    async def __call__(
        self, *args, outputs: Optional[Union[str, dict]] = None, error: Optional[str] = None
    ) -> AsyncSlackResponse:
        """Complete function for this request.

        Note: This function does NOT accept any positional arguments,
        it only ACCEPTS ONE KEYWORD ARGUMENT! A TypeError will be raised
        if this is not respected.

        Kwargs:
            outputs: Json serializable containing the output values
            error: Error message to return to slack

        Returns:
            SlackResponse: the response object returned from slack

        Raises:
            TypeError: If positional arguments are provided or more then 1
                keyword argument is provided.
        """

        if args:
            raise TypeError(
                f"{get_name_for_logging(self)} takes 0 positional arguments but "
                f"{len(args)} {'were' if len(args) > 1 else 'was'} given, "
                f"missing 1 keyword-only argument: {get_kwargs_for_logging(self)}"
            )

        if outputs is not None and error is not None:
            raise TypeError(
                f"{get_name_for_logging(self)} expects 1 keyword-only argument but 2 were given, "
                f"provide: {get_kwargs_for_logging(self)}"
            )

        if self.function_execution_id is None:
            raise ValueError(f"{get_name_for_logging(self)} is unsupported here as there is no function_execution_id")

        if isinstance(error, str):
            # TODO add this new api call to the sdk and use it here
            return await self.client.api_call(
                "functions.completeError", json={"error": error, "function_execution_id": self.function_execution_id}
            )

        # TODO add this new api call to the sdk and use it here
        return await self.client.api_call(
            "functions.completeSuccess",
            json={"outputs": outputs if outputs else {}, "function_execution_id": self.function_execution_id},
        )
