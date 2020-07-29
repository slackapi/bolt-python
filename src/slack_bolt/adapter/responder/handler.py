from typing import Optional

from responder.models import Request, Response

from slack_bolt import BoltRequest, App, BoltResponse
from slack_bolt.oauth import OAuthFlow


def to_bolt_request(req: Request, body: str) -> BoltRequest:
    return BoltRequest(
        body=body,
        query=req.url.query,
        headers=req.headers,
    )


def write_response(bolt_resp: BoltResponse, resp: Response):
    resp.status_code = bolt_resp.status
    resp.text = bolt_resp.body

    for key, value in bolt_resp.first_headers_without_set_cookie().items():
        resp.headers[key] = value

    for cookie in bolt_resp.cookies():
        for name, c in cookie.items():
            resp.set_cookie(
                key=name,
                value=c.value,
                max_age=c.get("max-age", None),
                expires=c.get("expires", None),
                path=c.get("path", None),
                domain=c.get("domain", None),
                secure=True,
                httponly=True,
            )


class SlackRequestHandler():
    def __init__(self, app: App):
        self.app = app

    async def handle(self, req: Request, resp: Response) -> Response:
        raw_body: Optional[bytes] = await req.content
        body: str = raw_body.decode("utf-8") if raw_body else ""
        method = req.method.upper()
        if method == "GET":
            if self.app.oauth_flow is not None:
                oauth_flow: OAuthFlow = self.app.oauth_flow
                if req.url.path == self.app.oauth_flow.install_path:
                    bolt_resp = oauth_flow.handle_installation(to_bolt_request(req, body))
                    write_response(bolt_resp, resp)
                    return
                elif req.url.path == self.app.oauth_flow.redirect_uri_path:
                    bolt_resp = oauth_flow.handle_callback(to_bolt_request(req, body))
                    write_response(bolt_resp, resp)
                    return

            resp.status_code = 404
            resp.text = "Not Found"
            return
        elif method == "POST":
            bolt_resp = self.app.dispatch(to_bolt_request(req, body))
            write_response(bolt_resp, resp)
            return

        resp.status_code = 404
        resp.text = "Not Found"
        return
