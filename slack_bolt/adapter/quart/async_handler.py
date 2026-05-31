from typing import Any, Dict, Optional, cast

from quart import Request, Response, make_response

from slack_bolt import BoltResponse
from slack_bolt.async_app import AsyncApp, AsyncBoltRequest
from slack_bolt.oauth.async_oauth_flow import AsyncOAuthFlow


async def to_async_bolt_request(
    req: Request,
    addition_context_properties: Optional[Dict[str, Any]] = None,
) -> AsyncBoltRequest:
    request = AsyncBoltRequest(
        body=cast(str, await req.get_data(as_text=True)),
        query=req.query_string.decode("utf-8"),
        headers=req.headers,  # type: ignore[arg-type]
    )

    if addition_context_properties is not None:
        for k, v in addition_context_properties.items():
            request.context[k] = v

    return request


async def to_quart_response(bolt_resp: BoltResponse) -> Response:
    resp = cast(Response, await make_response(bolt_resp.body, bolt_resp.status))
    for k, values in bolt_resp.headers.items():
        if k == "set-cookie":
            continue
        if k.lower() == "content-type" and resp.headers.get("content-type") is not None:
            resp.headers.pop("content-type")
        for v in values:
            resp.headers.add_header(k, v)

    for cookie in bolt_resp.cookies():
        for name, c in cookie.items():
            resp.set_cookie(
                key=name,
                value=c.value,
                max_age=c.get("max-age"),
                expires=c.get("expires"),
                path=c.get("path"),
                domain=c.get("domain"),
                secure=True,
                httponly=True,
            )

    return resp


class AsyncSlackRequestHandler:
    def __init__(self, app: AsyncApp):
        self.app = app

    async def handle(self, req: Request, addition_context_properties: Optional[Dict[str, Any]] = None) -> Response:
        if req.method == "POST":
            bolt_resp = await self.app.async_dispatch(await to_async_bolt_request(req, addition_context_properties))
            return await to_quart_response(bolt_resp)

        if req.method == "GET" and self.app.oauth_flow is not None:
            oauth_flow: AsyncOAuthFlow = self.app.oauth_flow
            bolt_req = await to_async_bolt_request(req, addition_context_properties)
            if req.path == oauth_flow.install_path:
                bolt_resp = await oauth_flow.handle_installation(bolt_req)
                return await to_quart_response(bolt_resp)
            if req.path == oauth_flow.redirect_uri_path:
                bolt_resp = await oauth_flow.handle_callback(bolt_req)
                return await to_quart_response(bolt_resp)

        return cast(Response, await make_response("Not Found", 404))
