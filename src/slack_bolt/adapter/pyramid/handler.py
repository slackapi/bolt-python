from pyramid.request import Request
from pyramid.response import Response

from slack_bolt import App, BoltRequest


class SlackRequestHandler():
    def __init__(self, app: App):
        self.app = app

    def handle(self, request: Request) -> Response:
        bolt_req = BoltRequest(
            body=request.body.decode("utf-8"),
            headers=request.headers,
        )
        bolt_resp = self.app.dispatch(bolt_req)
        return Response(
            status=bolt_resp.status,
            body=bolt_resp.body,
            headers=bolt_resp.headers
        )
