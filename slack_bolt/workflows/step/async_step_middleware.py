# mypy: ignore-errors
from typing import Callable, Optional, Awaitable

from slack_bolt.listener.async_listener import AsyncListener
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from slack_bolt.util.utils import get_name_for_callable
from slack_bolt.workflows.step.async_step import AsyncWorkflowStep


class AsyncWorkflowStepMiddleware(AsyncMiddleware):
    """Base middleware for step from app specific ones"""

    def __init__(self, step: AsyncWorkflowStep):
        self.step = step

    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:

        if await self.step.edit.async_matches(req=req, resp=resp):
            resp = await self._run(self.step.edit, req, resp)
            if resp is not None:
                return resp
        elif await self.step.save.async_matches(req=req, resp=resp):
            resp = await self._run(self.step.save, req, resp)
            if resp is not None:
                return resp
        elif await self.step.execute.async_matches(req=req, resp=resp):
            resp = await self._run(self.step.execute, req, resp)
            if resp is not None:
                return resp

        return await next()

    @staticmethod
    async def _run(
        listener: AsyncListener,
        req: AsyncBoltRequest,
        resp: BoltResponse,
    ) -> Optional[BoltResponse]:
        resp, next_was_not_called = await listener.run_async_middleware(req=req, resp=resp)
        if next_was_not_called:
            return None

        return await req.context.listener_runner.run(
            request=req,
            response=resp,
            listener_name=get_name_for_callable(listener.ack_function),
            listener=listener,
        )
