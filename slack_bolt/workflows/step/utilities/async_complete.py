from slack_sdk.web.async_client import AsyncWebClient


class AsyncComplete:
    def __init__(self, *, client: AsyncWebClient, body: dict):
        self.client = client
        self.body = body

    async def __call__(self, **kwargs) -> None:
        await self.client.workflows_stepCompleted(
            workflow_step_execute_id=self.body["event"]["workflow_step"][
                "workflow_step_execute_id"
            ],
            **kwargs,
        )
