from typing import Callable

from flask import Request, Response, make_response

from slack_bolt.app import App
from slack_bolt.error import BoltError
from slack_bolt.lazy_listener import LazyListenerRunner
from slack_bolt.oauth import OAuthFlow
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


def to_bolt_request(req: Request) -> BoltRequest:
    return BoltRequest(  # type: ignore
        body=req.get_data(as_text=True),
        query=req.query_string.decode("utf-8"),
        headers=req.headers,  # type: ignore
    )  # type: ignore


def to_flask_response(bolt_resp: BoltResponse) -> Response:
    resp: Response = make_response(bolt_resp.body, bolt_resp.status)
    for k, values in bolt_resp.headers.items():
        if k.lower() == "content-type" and resp.headers.get("content-type") is not None:
            # Remove the one set by Flask
            resp.headers.pop("content-type")
        for v in values:
            resp.headers.add_header(k, v)
    return resp


class NoopLazyListenerRunner(LazyListenerRunner):
    def start(self, function: Callable[..., None], request: BoltRequest) -> None:
        raise BoltError(
            "The google_cloud_functions adapter does not support lazy listeners. "
            "Please consider either having a queue to pass the request to a different function or "
            "rewriting your code not to use lazy listeners."
        )


class SlackRequestHandler:
    def __init__(self, app: App):  # type: ignore
        self.app = app
        # Note that lazy listener is not supported
        self.app.listener_runner.lazy_listener_runner = NoopLazyListenerRunner()
        if self.app.oauth_flow is not None:
            self.app.oauth_flow.settings.redirect_uri_page_renderer.install_path = "?"

    def handle(self, req: Request) -> Response:
        if req.method == "GET":
            if self.app.oauth_flow is not None:
                oauth_flow: OAuthFlow = self.app.oauth_flow
                bolt_req = to_bolt_request(req)
                if "code" in req.args or "error" in req.args or "state" in req.args:
                    bolt_resp = oauth_flow.handle_callback(bolt_req)
                    return to_flask_response(bolt_resp)
                else:
                    bolt_resp = oauth_flow.handle_installation(bolt_req)
                    return to_flask_response(bolt_resp)
        elif req.method == "POST":
            bolt_resp: BoltResponse = self.app.dispatch(to_bolt_request(req))
            return to_flask_response(bolt_resp)

        return make_response("Not Found", 404)
