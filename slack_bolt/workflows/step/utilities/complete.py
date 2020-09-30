from slack_sdk.web import WebClient


class Complete:
    def __init__(self, *, client: WebClient, body: dict):
        self.client = client
        self.body = body

    def __call__(self, **kwargs) -> None:
        self.client.workflows_stepCompleted(
            workflow_step_execute_id=self.body["event"]["workflow_step"][
                "workflow_step_execute_id"
            ],
            **kwargs,
        )
