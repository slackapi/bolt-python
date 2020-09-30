from slack_sdk.web.async_client import AsyncWebClient


class AsyncUpdate:
    def __init__(self, *, client: AsyncWebClient, body: dict):
        self.client = client
        self.body = body

    async def __call__(self, **kwargs) -> None:
        await self.client.workflows_updateStep(
            workflow_step_edit_id=self.body["workflow_step"]["workflow_step_edit_id"],
            **kwargs,
        )
