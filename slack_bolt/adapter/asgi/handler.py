import json
# from ...request.request import BoltRequest
# from ...response.response import BoltResponse


# def get_chunks(data: bytes):
#     for i in range(0, len(data), MAX_RESPONSE_CHUNK_SIZE):
#         yield data[i:i + MAX_RESPONSE_CHUNK_SIZE]
#     yield b''


class SlackRequestHandler():

    def __init__(self, *, app: str):
        self.app = app
        self.started = False

    def to_bolt_request(self, scope, receive):
        headers = self.to_dict(scope.get("headers", []))
        print(json.dumps(headers, indent=4))
        print(scope)

        # return BoltRequest(
        #     body=req.get_data(as_text=True),
        #     query=req.query_string.decode("utf-8"),
        #     headers=req.headers
        # )

    def to_dict(self, headers):
        return {header[0].decode("utf-8"): header[1].decode("utf-8") for header in headers}

    # async def send_asgi_response(self, bolt_resp: BoltResponse, send) -> None:
    #     await send({
    #         'type': 'http.response.start',
    #         'status': bolt_resp.status,
    #         'headers': bolt_resp.headers
    #     })

    async def _handle_http(self, scope, receive, send):
        method = scope.get("method", "")
        print(method)
        print(receive)
        print(send)
        if method == "GET":
            self.to_bolt_request(scope, receive)
            # if self.app.oauth_flow is not None:
            # oauth_flow: OAuthFlow = self.app.oauth_flow
            # if req.path == oauth_flow.install_path:
            #     bolt_resp = oauth_flow.handle_installation(to_bolt_request(req))
            #     return to_flask_response(bolt_resp)
            # elif req.path == oauth_flow.redirect_uri_path:
            #     bolt_resp = oauth_flow.handle_callback(to_bolt_request(req))
            #     return to_flask_response(bolt_resp)
        elif method == "POST":
            self.to_bolt_request(scope, receive)
            # bolt_resp: BoltResponse = self.app.dispatch(self.to_bolt_request(scope))
            # return to_flask_response(bolt_resp)

        # return make_response("Not Found", 404)

        # request = Request.incoming(
        #     scope["method"],
        #     scope["raw_path"],
        #     scope["query_string"],
        #     list(scope["headers"]),
        # )

        # request.scope = scope
        # request.content = ASGIContent(receive)

        # response = await self.handle(request)
        # await send_asgi_response(response, send)

        # request.scope = None  # type: ignore
        # request.content.dispose()

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            return await self._handle_http(scope, receive, send)

        raise TypeError(f"Unsupported scope type: {scope['type']}")


app = SlackRequestHandler(app="hello")
