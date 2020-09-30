from slack_sdk.web import WebClient


class Update:
    def __init__(self, *, client: WebClient, body: dict):
        self.client = client
        self.body = body

    def __call__(self, **kwargs) -> None:
        self.client.workflows_updateStep(
            workflow_step_edit_id=self.body["workflow_step"]["workflow_step_edit_id"],
            **kwargs,
        )
