from falcon import Request, Response

from slack_bolt.app import App
from slack_bolt.request import BoltRequest


class SlackAppResource():
    """
    from slack_bolt import App
    app = App()

    import falcon
    api = application = falcon.API()
    api.add_route("/slack/events", SlackAppResource(app))
    """

    def __init__(self, app: App):
        self.app = app

    def on_post(self, req: Request, resp: Response):
        slack_req = BoltRequest(
            body=req.stream.read(req.content_length or 0).decode("utf-8"),
            headers={k.lower(): v for k, v in req.headers.items()}
        )
        slack_resp = self.app.dispatch(slack_req)
        resp.body = slack_resp.body
        resp.status = str(slack_resp.status)
        resp.set_headers(slack_resp.headers)
