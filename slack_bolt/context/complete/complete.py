from typing import Optional, Union

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse
from slack_bolt.context.complete.internals import can_not_complete


class Complete:
    client: Optional[WebClient]
    function_execution_id: Optional[str]

    def __init__(
        self,
        client: Optional[WebClient],
        function_execution_id: Optional[str],
    ):
        self.client = client
        self.function_execution_id = function_execution_id

    def __call__(self, *args, outputs: Optional[Union[str, dict]] = None, error: Optional[str] = None) -> SlackResponse:
        if args:
            raise TypeError(
                f"{self._name()} takes 0 positional arguments but "
                f"{len(args)} {'were' if len(args) > 1 else 'was'} given, "
                f"missing 1 keyword-only argument: {self._get_kwargs_msg()}"
            )

        if outputs is not None and error is not None:
            raise TypeError(
                f"{self._name()} expects 1 keyword-only argument but 2 were given, " f"provide: {self._get_kwargs_msg()}"
            )

        if can_not_complete(self):
            raise ValueError(f"{self._name()} is unsupported here as there is no function_execution_id")

        if isinstance(outputs, dict) or isinstance(outputs, str):
            # TODO add this new api call to the sdk and use it here
            return self.client.api_call(
                "functions.completeSuccess",
                json={"outputs": outputs, "function_execution_id": self.function_execution_id},
            )

        if isinstance(error, str):
            # TODO add this new api call to the sdk and use it here
            return self.client.api_call(
                "functions.completeError", json={"error": error, "function_execution_id": self.function_execution_id}
            )

        # TODO add this new api call to the sdk and use it here
        return self.client.api_call(
            "functions.completeSuccess",
            json={"outputs": {}, "function_execution_id": self.function_execution_id},
        )

    def _get_kwargs_msg(self) -> str:
        separator = "', '"
        return f"'{separator.join(self.__call__.__kwdefaults__.keys())}' or no arguments"

    def _name(self) -> str:
        return f"{Complete.__name__.lower()}()"
