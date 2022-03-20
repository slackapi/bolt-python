from quart import Request, Response, make_response

from slack_bolt import BoltResponse
from slack_bolt.async_app import AsyncApp, AsyncBoltRequest
from slack_bolt.oauth.async_oauth_flow import AsyncOAuthFlow

async def to_async_bolt_request(req: Request) -> AsyncBoltRequest:
    body = await req.get_data(as_text=True)
    return AsyncBoltRequest(
        body=body,
        query=req.query_string.decode("utf-8"),
        headers=req.headers,
    )

async def to_quart_response(bolt_resp: BoltResponse) -> Response:
    resp = await make_response(bolt_resp.body, bolt_resp.status)
    for k, values in bolt_resp.headers.items():
        if k.lower() == "content-type" and resp.headers.get("content-type") is not None:
            # Remove the one set by Flask
            resp.headers.pop("content-type")
        for v in values:
            resp.headers.add_header(k, v)
    return resp

class AsyncSlackRequestHandler:
    def __init__(self, app: AsyncApp):  # type: ignore
        self.app = app

    async def handle(self, req: Request) -> Response:
        if req.method == "GET":
            if self.app.oauth_flow is not None:
                oauth_flow: AsyncOAuthFlow = self.app.oauth_flow
                if req.path == oauth_flow.install_path:
                    bolt_resp = await oauth_flow.handle_installation(
                        await to_async_bolt_request(req)
                    )
                    return await to_quart_response(bolt_resp)
                elif req.path == oauth_flow.redirect_uri_path:
                    bolt_resp = await oauth_flow.handle_callback(
                        await to_async_bolt_request(req)
                    )
                    return await to_quart_response(bolt_resp)

        elif req.method == "POST":
            bolt_resp = await self.app.async_dispatch(await to_async_bolt_request(req))
            return await to_quart_response(bolt_resp)

        return await make_response("Not Found", 404)
