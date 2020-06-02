from starlette.requests import Request
from starlette.responses import Response

from slack_bolt import BoltRequest, App


class SlackRequestHandler():
    def __init__(self, app: App):
        self.app = app

    async def handle(self, req: Request) -> Response:
        body = await req.body()
        bolt_req = BoltRequest(
            body=body.decode("utf-8"),
            headers=req.headers,
        )
        bolt_resp = self.app.dispatch(bolt_req)
        resp = Response(
            status_code=bolt_resp.status,
            content=bolt_resp.body,
            headers=bolt_resp.headers,
        )
        return resp
