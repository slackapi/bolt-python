import inspect
import json
import logging
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor
from functools import wraps
from http.server import SimpleHTTPRequestHandler, HTTPServer
from typing import List, Union, Pattern, Callable, Dict, Optional

from slack_bolt.listener.custom_listener import CustomListener
from slack_bolt.listener.listener import Listener
from slack_bolt.listener.url_verification import UrlVerificationListener
from slack_bolt.listener_matcher import CustomListenerMatcher
from slack_bolt.listener_matcher import builtins as builtin_matchers
from slack_bolt.listener_matcher.listener_matcher import ListenerMatcher
from slack_bolt.logger import get_bolt_app_logger, get_bolt_logger
from slack_bolt.middleware import \
    Middleware, \
    SslCheck, \
    RequestVerification, \
    SingleTeamAuthorization, \
    MultiTeamsAuthorization, \
    IgnoringSelfEvents, \
    CustomMiddleware
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk import WebClient


class App():

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        signing_secret: str = os.environ["SLACK_SIGNING_SECRET"],
        token: Optional[str] = os.environ.get("SLACK_BOT_TOKEN", None),
        verification_token: Optional[str] = os.environ.get("SLACK_VERIFICATION_TOKEN", None),
        process_before_response: bool = False,
    ):
        self.name = name or inspect.stack()[1].filename.split(os.path.sep)[-1]
        self._signing_secret = signing_secret
        self._token = token
        self._verification_token = verification_token

        self._client = WebClient(token=token)  # TODO pooling per token
        self._framework_logger = get_bolt_logger(App)

        self._middleware_list: List[Middleware] = []
        self._listeners: List[Listener] = []
        self._listener_executor = ThreadPoolExecutor(max_workers=5)  # TODO: shutdown
        self._process_before_response = process_before_response

        self._init_middleware_list_done = False
        self._init_middleware_list()
        self._init_listeners_done = False
        self._init_listeners()

    def _init_middleware_list(self):
        if self._init_middleware_list_done:
            return
        self._middleware_list.append(SslCheck(verification_token=self._verification_token))
        self._middleware_list.append(RequestVerification(self._signing_secret))
        if self._token:
            self._middleware_list.append(SingleTeamAuthorization(self._client))
        else:
            self._middleware_list.append(MultiTeamsAuthorization())  # TODO
        self._middleware_list.append(IgnoringSelfEvents())
        self._init_middleware_list_done = True

    def _init_listeners(self):
        if self._init_listeners_done:
            return
        self._listeners.append(UrlVerificationListener())
        self._init_listeners_done = True

    # -------------------------
    # standalone server

    def start(self, port: int = 3000, path: str = "/slack/events") -> None:
        self.server = SlackAppServer(app=self, port=port, path=path)
        self.server.start()

    # -------------------------
    # main dispatcher

    def dispatch(self, req: BoltRequest) -> BoltResponse:
        self._init_context(req)

        resp: BoltResponse = BoltResponse(status=200, body=None)
        middleware_state = {"next_called": False}

        def middleware_next():
            middleware_state["next_called"] = True

        for middleware in self._middleware_list:
            middleware_state["next_called"] = False
            if self._framework_logger.level <= logging.DEBUG:
                self._framework_logger.debug(f"Applying {middleware.name}")
            resp = middleware.process(req=req, resp=resp, next=middleware_next)
            if not middleware_state["next_called"]:
                return resp

        for listener in self._listeners:
            if listener.matches(req=req, resp=resp):
                listener_name = listener.func.__name__
                self._framework_logger.debug(f"Starting listener: {listener_name}")
                ack = req.context.ack
                starting_time = time.time()
                if self._process_before_response:
                    returned_value = listener(req=req, resp=resp)
                    if isinstance(returned_value, BoltResponse):
                        resp = returned_value
                else:
                    # start the listener function asynchronously
                    self._listener_executor.submit(lambda: listener(req=req, resp=resp))
                    while ack.response is None and time.time() - starting_time <= 3:
                        time.sleep(0.01)

                if self._process_before_response:
                    if ack.response is None:
                        return resp
                    else:
                        return ack.response
                else:
                    if resp is None and ack.response is not None:
                        resp = ack.response
                        millis = int((time.time() - starting_time) * 1000)
                        self._framework_logger.debug(
                            f"Responding with status: {resp.status} body: \"{resp.body}\" ({millis} millis)")
                        return resp
                    else:
                        self._framework_logger.warning(f"{listener_name} didn't call ack()")

        self._framework_logger.warning(f"Unhandled request ({req.payload})")
        return BoltResponse(status=404, body={"error": "unhandled request"})

    # -------------------------
    # middleware

    def use(self, *args):
        return self.middleware(*args)

    def middleware(self, *args):
        if len(args) > 0:
            func = args[0]
            self._middleware_list.append(CustomMiddleware(app_name=self.name, func=func))

    # -------------------------
    # events

    def event(self, event_type: Union[str, Pattern], matchers: List[Callable[..., bool]] = []):
        def __call__(func):
            primary_matcher = builtin_matchers.event(event_type)
            return self._register_listener(func, primary_matcher, matchers)

        return __call__

    # -------------------------
    # slash commands

    def command(self, command: Union[str, Pattern], matchers: List[Callable[..., bool]] = []):
        def __call__(func):
            primary_matcher = builtin_matchers.command(command)
            return self._register_listener(func, primary_matcher, matchers)

        return __call__

    # -------------------------
    # shortcut

    def shortcut(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: List[Callable[..., bool]] = []):
        def __call__(func):
            primary_matcher = builtin_matchers.shortcut(constraints)
            return self._register_listener(func, primary_matcher, matchers)

        return __call__

    def global_shortcut(
        self,
        callback_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = []):
        def __call__(func):
            primary_matcher = builtin_matchers.global_shortcut(callback_id)
            return self._register_listener(func, primary_matcher, matchers)

        return __call__

    def message_shortcut(
        self,
        callback_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = []):
        def __call__(func):
            primary_matcher = builtin_matchers.message_shortcut(callback_id)
            return self._register_listener(func, primary_matcher, matchers)

        return __call__

    # -------------------------
    # action

    def action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: List[Callable[..., bool]] = []):
        def __call__(func):
            primary_matcher = builtin_matchers.action(constraints)
            return self._register_listener(func, primary_matcher, matchers)

        return __call__

    def block_action(self, action_id: Union[str, Pattern], matchers: List[Callable[..., bool]] = []):
        def __call__(func):
            primary_matcher = builtin_matchers.block_action(action_id)
            return self._register_listener(func, primary_matcher, matchers)

        return __call__

    # -------------------------
    # view

    def view(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: List[Callable[..., bool]] = []):
        def __call__(func):
            primary_matcher = builtin_matchers.view(constraints)
            return self._register_listener(func, primary_matcher, matchers)

        return __call__

    # -------------------------
    # options

    def options(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: List[Callable[..., bool]] = []):
        def __call__(func):
            primary_matcher = builtin_matchers.options(constraints)
            return self._register_listener(func, primary_matcher, matchers)

        return __call__

    def block_suggestion(
        self,
        action_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = []):
        def __call__(func):
            primary_matcher = builtin_matchers.block_suggestion(action_id)
            return self._register_listener(func, primary_matcher, matchers)

        return __call__

    def dialog_suggestion(
        self,
        callback_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = []):
        def __call__(func):
            primary_matcher = builtin_matchers.dialog_suggestion(callback_id)
            return self._register_listener(func, primary_matcher, matchers)

        return __call__

    # -------------------------

    def _init_context(self, req: BoltRequest):
        req.context["logger"] = get_bolt_app_logger(self.name)
        req.context["token"] = self._token
        req.context["client"] = self._client

    def _register_listener(
        self,
        func,
        primary_matcher: ListenerMatcher,
        matchers: List[Callable[..., bool]],
    ) -> Callable[..., None]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        listener_matchers = [CustomListenerMatcher(app_name=self.name, func=f) for f in matchers]
        listener_matchers.insert(0, primary_matcher)
        self._listeners.append(CustomListener(app_name=self.name, func=func, matchers=listener_matchers))
        return wrapper


# -------------------------

class SlackAppServer:
    def __init__(self, port: int, path: str, app: App):
        self.port = port
        _path = path
        _app = app

        class SlackAppHandler(SimpleHTTPRequestHandler):
            protocol_version = "HTTP/1.1"
            default_request_version = "HTTP/1.1"

            def do_POST(self):
                if _path != self.path.split('?')[0]:
                    self.send_response(404)
                    return

                len_header = self.headers.get("Content-Length") or 0
                content_len = int(len_header)
                request_body = self.rfile.read(content_len).decode("utf-8")
                bolt_req = BoltRequest(body=request_body, headers=self.headers)
                bolt_resp: BoltResponse = _app.dispatch(bolt_req)

                self.send_response(bolt_resp.status)

                response_body = bolt_resp.body if isinstance(bolt_resp.body, str) \
                    else json.dumps(bolt_resp.body)
                body_bytes = response_body.encode("utf-8")

                for k, v in bolt_resp.headers.items():
                    self.send_header(k, v)
                self.send_header("Content-Length", len(body_bytes))
                self.end_headers()
                self.wfile.write(body_bytes)
                return

        self.server = HTTPServer(('localhost', self.port), SlackAppHandler)

    def start(self):
        print("⚡️ Bolt app is running!")
        try:
            self.server.serve_forever(0.05)
        finally:
            self.server.server_close()
