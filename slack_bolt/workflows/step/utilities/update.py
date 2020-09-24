from slack_sdk.web import WebClient


class Update:
    def __init__(self, *, client: WebClient, body: dict):
        self.client = client
        self.body = body

    def __call__(self, *, inputs: dict, outputs: list,) -> None:
        self.client.workflows_updateStep(
            workflow_step_edit_id=self.body["workflow_step"]["workflow_step_edit_id"],
            inputs=inputs,
            outputs=outputs,
        )
