from typing import Union
from .http_request import AsgiHttpRequest

from slack_bolt import App
from slack_bolt.async_app import AsyncApp

from slack_bolt.async_app import AsyncBoltRequest
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class SlackRequestHandler:
    def __init__(self, app: Union[App, AsyncApp]):
        self.app = app
        if isinstance(app, AsyncApp):
            self.dispatch = self._async_dispatch
        self.dispatch = self._dispatch

    async def _dispatch(self, request: AsgiHttpRequest) -> BoltResponse:
        raw_body = await request.get_raw_body()
        return self.app.dispatch(BoltRequest(body=raw_body, query=request.query_string, headers=request.headers))

    async def _async_dispatch(self, request: AsgiHttpRequest) -> BoltResponse:
        raw_body = await request.get_raw_body()
        return self.app.async_dispatch(AsyncBoltRequest(body=raw_body, query=request.query_string, headers=request.headers))

    async def _handle_http(self, scope, receive, send):
        asgi_request = AsgiHttpRequest(scope, receive)
        if asgi_request.method == "GET":
            print("this is a get")
            # if self.app.oauth_flow is not None:
            # oauth_flow: OAuthFlow = self.app.oauth_flow
            # if req.path == oauth_flow.install_path:
            #     bolt_resp = oauth_flow.handle_installation(to_bolt_request(req))
            #     return to_flask_response(bolt_resp)
            # elif req.path == oauth_flow.redirect_uri_path:
            #     bolt_resp = oauth_flow.handle_callback(to_bolt_request(req))
            #     return to_flask_response(bolt_resp)
        elif asgi_request.method == "POST":
            bolt_response: BoltResponse = await self.dispatch(asgi_request)
            print(bolt_response.status)
            print(bolt_response.headers)
            print(bolt_response.body)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            return await self._handle_http(scope, receive, send)

        raise TypeError(f"Unsupported scope type: {scope['type']}")
