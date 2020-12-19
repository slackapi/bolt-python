from slack_sdk.web import WebClient


class Fail:
    def __init__(self, *, client: WebClient, body: dict):
        self.client = client
        self.body = body

    def __call__(
        self,
        *,
        error: dict,
    ) -> None:
        self.client.workflows_stepFailed(
            workflow_step_execute_id=self.body["event"]["workflow_step"][
                "workflow_step_execute_id"
            ],
            error=error,
        )
