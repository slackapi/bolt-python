from flask import Request, Response, make_response

from slack_bolt.app import App
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class SlackRequestHandler():
    def __init__(self, app: App):
        self.app = app

    def handle(self, req: Request) -> Response:
        slack_req: BoltRequest = BoltRequest(
            body=req.get_data(as_text=True),
            headers={k.lower(): v for k, v in req.headers.items()}
        )
        slack_resp: BoltResponse = self.app.dispatch(slack_req)
        resp: Response = make_response(slack_resp.body, slack_resp.status)
        for k, v in slack_resp.headers.items():
            resp.headers.add_header(k, v)
        return resp
