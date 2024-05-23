from typing import Any, Callable, Dict, Iterable, List, Tuple, Union
from slack_bolt.oauth.oauth_flow import OAuthFlow
from slack_bolt.adapter.wsgi.http_request import WsgiHttpRequest
from slack_bolt.adapter.wsgi.http_response import WsgiHttpResponse

from slack_bolt import App

from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse

scope_value_type = Union[str, bytes, Iterable[Tuple[bytes, bytes]]]

scope_type = Dict[str, scope_value_type]

class SlackRequestHandler():
    def __init__(self, app: App, path: str = "/slack/events"):  # type: ignore
        """Setup Bolt as an ASGI web framework, this will make your application compatible with ASGI web servers.
        This can be used for production deployment.

        With the default settings, `http://localhost:3000/slack/events`
        Run Bolt with [gunicorn](https://gunicorn.org/)

            # Python
            app = App()
            api = SlackRequestHandler(app)

            # bash
            export SLACK_SIGNING_SECRET=***
            export SLACK_BOT_TOKEN=xoxb-***
            gunicorn app:api -b 0.0.0.0:3000 --log-level debug

        Args:
            app: Your bolt application
            path: The path to handle request from Slack (Default: `/slack/events`)
        """
        self.path = path
        self.app = app

    def dispatch(self, request: WsgiHttpRequest) -> BoltResponse:
        return self.app.dispatch(
            BoltRequest(body=request.get_raw_body(), query=request.query_string, headers=request.get_headers())
        )

    def handle_installation(self, request: WsgiHttpRequest) -> BoltResponse:
        oauth_flow: OAuthFlow = self.app.oauth_flow
        return oauth_flow.handle_installation(
            BoltRequest(body=request.get_raw_body(), query=request.query_string, headers=request.get_headers())
        )

    def handle_callback(self, request: WsgiHttpRequest) -> BoltResponse:
        oauth_flow: OAuthFlow = self.app.oauth_flow
        return oauth_flow.handle_callback(
            BoltRequest(body=request.get_raw_body(), query=request.query_string, headers=request.get_headers())
        )

    def _get_http_response(self, method: str, path: str, request: WsgiHttpRequest) -> WsgiHttpResponse:
        if method == "GET":
            if self.app.oauth_flow is not None:
                if path == self.app.oauth_flow.install_path:
                    bolt_response: BoltResponse = self.handle_installation(request)
                    return WsgiHttpResponse(
                        status=bolt_response.status, headers=bolt_response.headers, body=bolt_response.body
                    )
                if path == self.app.oauth_flow.redirect_uri_path:
                    bolt_response: BoltResponse = self.handle_callback(request)
                    return WsgiHttpResponse(
                        status=bolt_response.status, headers=bolt_response.headers, body=bolt_response.body
                    )
        if method == "POST" and path == self.path:
            bolt_response: BoltResponse = self.dispatch(request)
            return WsgiHttpResponse(status=bolt_response.status, headers=bolt_response.headers, body=bolt_response.body)
        return WsgiHttpResponse(status=404, headers={"content-type": ["text/plain;charset=utf-8"]}, body="Not Found")

    def __call__( self, environ: Dict[str, Any], start_response: Callable[[str, List[Tuple[str, str]]], Callable[[bytes], object]]) -> Iterable[bytes]:
        print(environ)
        if "HTTP" in environ.get("SERVER_PROTOCOL", ""):
            response: WsgiHttpResponse = self._get_http_response(
                method=environ.get("REQUEST_METHOD", "GET"), path=environ.get("PATH_INFO", ""), request=WsgiHttpRequest(environ)
            )
            start_response(response.status, response.raw_headers)
            for test in response.body:
                print(test.decode("utf-8"))
            return response.body
        raise TypeError(f"Unsupported SERVER_PROTOCOL: {environ["SERVER_PROTOCOL"]}")
