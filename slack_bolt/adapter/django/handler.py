from typing import Optional

from django.http import HttpRequest, HttpResponse

from slack_bolt.app import App
from slack_bolt.oauth import OAuthFlow
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


def to_bolt_request(req: HttpRequest) -> BoltRequest:
    raw_body: bytes = req.body
    body: str = raw_body.decode("utf-8") if raw_body else ""
    return BoltRequest(
        body=body,
        query=req.META["QUERY_STRING"],
        headers=req.headers,
    )


def to_django_response(bolt_resp: BoltResponse) -> HttpResponse:
    resp: HttpResponse = HttpResponse(
        status=bolt_resp.status,
        content=bolt_resp.body.encode("utf-8"),
    )
    for k, v in bolt_resp.first_headers_without_set_cookie().items():
        resp[k] = v

    for cookie in bolt_resp.cookies():
        for name, c in cookie.items():
            str_max_age: Optional[str] = c.get("max-age")
            max_age: Optional[int] = int(str_max_age) if str_max_age else None
            resp.set_cookie(
                key=name,
                value=c.value,
                expires=c.get("expires"),
                max_age=max_age,
                domain=c.get("domain"),
                path=c.get("path"),
                secure=True,
                httponly=True,
            )
    return resp


class SlackRequestHandler:
    def __init__(self, app: App):  # type: ignore
        self.app = app

    def handle(self, req: HttpRequest) -> HttpResponse:
        if req.method == "GET":
            if self.app.oauth_flow is not None:
                oauth_flow: OAuthFlow = self.app.oauth_flow
                if req.path == oauth_flow.install_path:
                    bolt_resp = oauth_flow.handle_installation(to_bolt_request(req))
                    return to_django_response(bolt_resp)
                elif req.path == oauth_flow.redirect_uri_path:
                    bolt_resp = oauth_flow.handle_callback(to_bolt_request(req))
                    return to_django_response(bolt_resp)
        elif req.method == "POST":
            bolt_resp: BoltResponse = self.app.dispatch(to_bolt_request(req))
            return to_django_response(bolt_resp)

        return HttpResponse(status=404, content=b"Not Found")
