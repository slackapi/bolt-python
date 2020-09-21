import logging

from aiohttp import web

from slack_bolt.adapter.aiohttp import to_bolt_request, to_aiohttp_response
from slack_bolt.response import BoltResponse


class AsyncSlackAppServer:
    def __init__(
        self, port: int, path: str, app,  # AsyncApp
    ):
        """Standalone AIOHTTP Web Server

        Refer to AIOHTTP documents for details.
        https://docs.aiohttp.org/en/stable/web.html
        """
        self._port = port
        self._endpoint_path = path
        self._bolt_app: "AsyncApp" = app

        self.web_app = web.Application()
        self._bolt_oauth_flow = self._bolt_app.oauth_flow
        if self._bolt_oauth_flow:
            self.web_app.add_routes(
                [
                    web.get(
                        self._bolt_oauth_flow.install_path, self.handle_get_requests
                    ),
                    web.get(
                        self._bolt_oauth_flow.redirect_uri_path,
                        self.handle_get_requests,
                    ),
                    web.post(self._endpoint_path, self.handle_post_requests),
                ]
            )
        else:
            self.web_app.add_routes(
                [web.post(self._endpoint_path, self.handle_post_requests)]
            )

    async def handle_get_requests(self, request: web.Request) -> web.Response:
        oauth_flow = self._bolt_oauth_flow
        if oauth_flow:
            if request.path == oauth_flow.install_path:
                bolt_req = await to_bolt_request(request)
                bolt_resp = await oauth_flow.handle_installation(bolt_req)
                return await to_aiohttp_response(bolt_resp)
            elif request.path == oauth_flow.redirect_uri_path:
                bolt_req = await to_bolt_request(request)
                bolt_resp = await oauth_flow.handle_callback(bolt_req)
                return await to_aiohttp_response(bolt_resp)
            else:
                return web.Response(status=404)
        else:
            return web.Response(status=404)

    async def handle_post_requests(self, request: web.Request) -> web.Response:
        if self._endpoint_path != request.path:
            return web.Response(status=404)

        bolt_req = await to_bolt_request(request)
        bolt_resp: BoltResponse = await self._bolt_app.async_dispatch(bolt_req)
        return await to_aiohttp_response(bolt_resp)

    def start(self) -> None:
        """ Starts a new web server process.

        :return: None
        """
        if self._bolt_app.logger.level > logging.INFO:
            print("⚡️ Bolt app is running!")
        else:
            self._bolt_app.logger.info("⚡️ Bolt app is running!")

        web.run_app(self.web_app, host="0.0.0.0", port=self._port)
