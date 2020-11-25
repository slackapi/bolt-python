import logging
from time import time

from slack_sdk.socket_mode.async_client import AsyncBaseSocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


async def run_async_bolt_app(app: AsyncApp, req: SocketModeRequest):
    bolt_req: AsyncBoltRequest = AsyncBoltRequest(mode="socket_mode", body=req.payload)
    bolt_resp: BoltResponse = await app.async_dispatch(bolt_req)
    return bolt_resp


async def send_async_response(
    client: AsyncBaseSocketModeClient,
    req: SocketModeRequest,
    bolt_resp: BoltResponse,
    start_time: int,
):
    if bolt_resp.status == 200:
        if bolt_resp.body is None or len(bolt_resp.body) == 0:
            await client.send_socket_mode_response(
                SocketModeResponse(envelope_id=req.envelope_id)
            )
        elif bolt_resp.body.startswith("{"):
            await client.send_socket_mode_response(
                SocketModeResponse(envelope_id=req.envelope_id, payload=bolt_resp.body,)
            )
        else:
            await client.send_socket_mode_response(
                SocketModeResponse(
                    envelope_id=req.envelope_id, payload={"text": bolt_resp.body},
                )
            )
        if client.logger.level <= logging.DEBUG:
            spent_time = int((time() - start_time) * 1000)
            client.logger.debug(f"Response time: {spent_time} milliseconds")
    else:
        client.logger.info(
            f"Unsuccessful Bolt execution result (status: {bolt_resp.status}, body: {bolt_resp.body})"
        )
