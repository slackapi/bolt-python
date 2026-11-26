from datetime import datetime
from typing import Any, Dict, Optional

from sanic.request import Request
from sanic.response import HTTPResponse

from slack_bolt import BoltResponse
from slack_bolt.async_app import AsyncApp, AsyncBoltRequest
from slack_bolt.oauth.async_oauth_flow import AsyncOAuthFlow


def to_async_bolt_request(req: Request, addition_context_properties: Optional[Dict[str, Any]] = None) -> AsyncBoltRequest:
    request = AsyncBoltRequest(
        body=req.body.decode("utf-8"),
        query=req.query_string,
        headers=req.headers,  # type: ignore[arg-type]
    )

    if addition_context_properties is not None:
        for k, v in addition_context_properties.items():
            request.context[k] = v

    return request


def to_sanic_response(bolt_resp: BoltResponse) -> HTTPResponse:
    resp = HTTPResponse(
        status=bolt_resp.status,
        body=bolt_resp.body,
        headers=bolt_resp.first_headers_without_set_cookie(),
    )

    for cookie in bolt_resp.cookies():
        for key, c in cookie.items():
            expire_value = c.get("expires")
            expires = datetime.strptime(expire_value, "%a, %d %b %Y %H:%M:%S %Z") if expire_value else None
            max_age = int(c["max-age"]) if c.get("max-age") else None
            path = str(c.get("path")) if c.get("path") else "/"
            domain = str(c.get("domain")) if c.get("domain") else None
            resp.add_cookie(
                key=key,
                value=c.value,
                expires=expires,
                path=path,
                domain=domain,
                max_age=max_age,
                secure=True,
                httponly=True,
            )

    return resp


class AsyncSlackRequestHandler:
    def __init__(self, app: AsyncApp):
        self.app = app

    async def handle(self, req: Request, addition_context_properties: Optional[Dict[str, Any]] = None) -> HTTPResponse:
        if req.method == "GET":
            if self.app.oauth_flow is not None:
                oauth_flow: AsyncOAuthFlow = self.app.oauth_flow
                if req.path == oauth_flow.install_path:
                    bolt_resp = await oauth_flow.handle_installation(to_async_bolt_request(req, addition_context_properties))
                    return to_sanic_response(bolt_resp)
                elif req.path == oauth_flow.redirect_uri_path:
                    bolt_resp = await oauth_flow.handle_callback(to_async_bolt_request(req, addition_context_properties))
                    return to_sanic_response(bolt_resp)

        elif req.method == "POST":
            bolt_resp = await self.app.async_dispatch(to_async_bolt_request(req, addition_context_properties))
            return to_sanic_response(bolt_resp)

        return HTTPResponse(
            status=404,
            body="Not found",
        )
