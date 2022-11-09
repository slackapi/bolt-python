from typing import Callable, Iterable, Tuple, Dict, Union
from slack_bolt.oauth.async_oauth_flow import AsyncOAuthFlow

from slack_bolt.oauth.oauth_flow import OAuthFlow
from .http_request import AsgiHttpRequest
from .http_response import AsgiHttpResponse

from slack_bolt import App
from slack_bolt.async_app import AsyncApp

from slack_bolt.async_app import AsyncBoltRequest
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class SlackRequestHandler:
    def __init__(self, app: Union[App, AsyncApp], path: str = "/slack/events"):
        self.path = path
        self.app = app
        if isinstance(app, AsyncApp):
            self.dispatch = self._async_dispatch
            self.handle_installation = self._async_handle_installation
            self.handle_callback = self._async_handle_callback
        else:
            self.dispatch = self._dispatch
            self.handle_installation = self._handle_installation
            self.handle_callback = self._handle_callback

    async def _dispatch(self, request: AsgiHttpRequest) -> BoltResponse:
        raw_body = await request.get_raw_body()
        return self.app.dispatch(BoltRequest(body=raw_body, query=request.query_string, headers=request.headers))

    async def _handle_installation(self, request: AsgiHttpRequest) -> BoltResponse:
        oauth_flow: OAuthFlow = self.app.oauth_flow
        raw_body = await request.get_raw_body()
        return oauth_flow.handle_installation(
            BoltRequest(body=raw_body, query=request.query_string, headers=request.headers)
        )

    async def _handle_callback(self, request: AsgiHttpRequest) -> BoltResponse:
        oauth_flow: OAuthFlow = self.app.oauth_flow
        raw_body = await request.get_raw_body()
        return oauth_flow.handle_callback(BoltRequest(body=raw_body, query=request.query_string, headers=request.headers))

    async def _async_dispatch(self, request: AsgiHttpRequest) -> BoltResponse:
        raw_body = await request.get_raw_body()
        return await self.app.async_dispatch(
            AsyncBoltRequest(body=raw_body, query=request.query_string, headers=request.headers)
        )

    async def _async_handle_installation(self, request: AsgiHttpRequest) -> BoltResponse:
        oauth_flow: AsyncOAuthFlow = self.app.oauth_flow
        raw_body = await request.get_raw_body()
        return await oauth_flow.handle_installation(
            BoltRequest(body=raw_body, query=request.query_string, headers=request.headers)
        )

    async def _async_handle_callback(self, request: AsgiHttpRequest) -> BoltResponse:
        oauth_flow: AsyncOAuthFlow = self.app.oauth_flow
        raw_body = await request.get_raw_body()
        return await oauth_flow.handle_callback(
            BoltRequest(body=raw_body, query=request.query_string, headers=request.headers)
        )

    async def _send_http_response(self, response: AsgiHttpResponse, send: Callable) -> None:
        await send(response.get_response_start())
        await send(response.get_response_body())

    async def _get_http_response(self, request: AsgiHttpRequest) -> AsgiHttpResponse:
        if request.method == "GET":
            if self.app.oauth_flow is not None:
                if request.path == self.app.oauth_flow.install_path:
                    bolt_response: BoltResponse = await self.handle_installation(request)
                    return AsgiHttpResponse(
                        status=bolt_response.status, headers=bolt_response.headers, body=bolt_response.body
                    )
                if request.path == self.app.oauth_flow.redirect_uri_path:
                    bolt_response: BoltResponse = await self.handle_callback(request)
                    return AsgiHttpResponse(
                        status=bolt_response.status, headers=bolt_response.headers, body=bolt_response.body
                    )
        if request.method == "POST" and request.path == self.path:
            bolt_response: BoltResponse = await self.dispatch(request)
            return AsgiHttpResponse(status=bolt_response.status, headers=bolt_response.headers, body=bolt_response.body)
        return AsgiHttpResponse(status=404, headers={"content-type": ["text/plain;charset=utf-8"]}, body="Not Found")

    async def __call__(
        self, scope: Dict[str, Union[str, bytes, Iterable[Tuple[bytes, bytes]]]], receive: Callable, send: Callable
    ) -> None:
        if scope["type"] == "http":
            request = AsgiHttpRequest(scope, receive)
            response: AsgiHttpResponse = await self._get_http_response(request)
            return await self._send_http_response(response, send)

        raise TypeError(f"Unsupported scope type: {scope['type']}")
