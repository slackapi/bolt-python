import inspect
import json
import logging
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor
from functools import wraps
from http.server import SimpleHTTPRequestHandler, HTTPServer
from typing import List, Union, Pattern, Callable, Dict, Optional
from urllib.parse import parse_qs

from slack_bolt.listener.custom_listener import CustomListener
from slack_bolt.listener.listener import Listener
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
from slack_bolt.middleware.url_verification import UrlVerification
from slack_bolt.oauth import OAuthFlow
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk import WebClient
from slack_sdk.oauth import OAuthStateUtils
from slack_sdk.oauth.installation_store import InstallationStore, FileInstallationStore
from slack_sdk.oauth.state_store import OAuthStateStore, FileOAuthStateStore


class App():

    def __init__(
        self,
        *,
        # Used in logger
        name: Optional[str] = None,
        # Set True when you run this app on a FaaS platform
        process_before_response: bool = False,
        # Basic Information > Credentials > Signing Secret
        signing_secret: str = os.environ.get("SLACK_SIGNING_SECRET", None),
        # for single-workspace apps
        token: Optional[str] = os.environ.get("SLACK_BOT_TOKEN", None),
        client: Optional[WebClient] = None,
        # for multi-workspace apps
        installation_store: Optional[InstallationStore] = None,
        oauth_state_store: Optional[OAuthStateStore] = None,
        oauth_state_cookie_name: str = OAuthStateUtils.default_cookie_name,
        oauth_state_expiration_seconds: int = OAuthStateUtils.default_expiration_seconds,

        # for the OAuth flow
        oauth_flow: Optional[OAuthFlow] = None,
        client_id: Optional[str] = os.environ.get("SLACK_CLIENT_ID", None),
        client_secret: Optional[str] = os.environ.get("SLACK_CLIENT_SECRET", None),
        scopes: List[str] = os.environ.get("SLACK_SCOPES", "").split(","),
        user_scopes: List[str] = os.environ.get("SLACK_USER_SCOPES", "").split(","),
        redirect_uri: Optional[str] = os.environ.get("SLACK_REDIRECT_URI", None),
        oauth_install_path: str = os.environ.get("SLACK_INSTALL_PATH", "/slack/install"),
        oauth_redirect_uri_path: str = os.environ.get("SLACK_REDIRECT_URI_PATH", "/slack/oauth_redirect"),
        oauth_success_url: Optional[str] = None,
        oauth_failure_url: Optional[str] = None,

        # No need to set (the value is used only in response to ssl_check requests)
        verification_token: Optional[str] = os.environ.get("SLACK_VERIFICATION_TOKEN", None),
    ):
        self.name = name or inspect.stack()[1].filename.split(os.path.sep)[-1]
        self._signing_secret: str = signing_secret
        self._verification_token: Optional[str] = verification_token
        self._framework_logger = get_bolt_logger(App)

        self._token: Optional[str] = token

        if client is not None:
            self._client = client
            self._token = client.token
            if token is not None:
                self._framework_logger.warning(
                    "As you gave client as well, the bot token will be unused.")
        else:
            self._client = WebClient(token=token)  # NOTE: the token here can be None

        self._installation_store: Optional[InstallationStore] = installation_store
        self._oauth_state_store: Optional[OAuthStateStore] = oauth_state_store
        if self._installation_store.logger is None:
            self._installation_store.logger = self._framework_logger
        if self._oauth_state_store.logger is None:
            self._oauth_state_store.logger = self._framework_logger

        self._oauth_state_cookie_name = oauth_state_cookie_name
        self._oauth_state_expiration_seconds = oauth_state_expiration_seconds

        self.oauth_flow: Optional[OAuthFlow] = None
        if oauth_flow:
            self.oauth_flow = oauth_flow
            self._sync_client_logger_with_oauth_flow()
            if self._installation_store is None:
                self._installation_store = self.oauth_flow.installation_store
        else:
            if client_id is not None and client_secret is not None:
                # The OAuth flow support is enabled
                if self._installation_store is None and self._oauth_state_store is None:
                    # use the default ones
                    self._installation_store = FileInstallationStore(
                        logger=self._framework_logger,
                        client_id=client_id,
                    )
                    self._oauth_state_store = FileOAuthStateStore(
                        logger=self._framework_logger,
                        expiration_seconds=self._oauth_state_expiration_seconds,
                        client_id=client_id,
                    )

                if self._installation_store is not None and self._oauth_state_store is None:
                    raise ValueError(f"Configure an appropriate OAuthStateStore for {self._installation_store}")

                self.oauth_flow = OAuthFlow(
                    client=WebClient(token=None),
                    logger=self._framework_logger,
                    # required storage implementations
                    installation_store=self._installation_store,
                    oauth_state_store=self._oauth_state_store,
                    oauth_state_cookie_name=self._oauth_state_cookie_name,
                    oauth_state_expiration_seconds=self._oauth_state_expiration_seconds,
                    # used for oauth.v2.access calls
                    client_id=client_id,
                    client_secret=client_secret,
                    # installation url parameters
                    scopes=scopes,
                    user_scopes=user_scopes,
                    redirect_uri=redirect_uri,
                    # path in this app
                    install_path=oauth_install_path,
                    redirect_uri_path=oauth_redirect_uri_path,
                    # urls after callback
                    success_url=oauth_success_url,
                    failure_url=oauth_failure_url,
                )

        if self._installation_store is not None and self._token is not None:
            self._token = None
            self._framework_logger.warning(
                "As you gave installation_store as well, the bot token will be unused.")

        self._middleware_list: List[Union[Callable, Middleware]] = []
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
        if self.oauth_flow is None and self._token:
            self._middleware_list.append(SingleTeamAuthorization())
        else:
            self._middleware_list.append(MultiTeamsAuthorization(self._installation_store))
        self._middleware_list.append(IgnoringSelfEvents())
        self._middleware_list.append(UrlVerification())
        self._init_middleware_list_done = True

    def _init_listeners(self):
        if self._init_listeners_done:
            return
        self._init_listeners_done = True

    def _sync_client_logger_with_oauth_flow(self):
        if self.oauth_flow.client is None:
            self.oauth_flow.client = self._client
        if self.oauth_flow.logger is None:
            self.oauth_flow.logger = self._framework_logger
            if self.oauth_flow.installation_store.logger is None:
                self.oauth_flow.installation_store.logger = self._framework_logger
            if self.oauth_flow.oauth_state_store.logger is None:
                self.oauth_flow.oauth_state_store.logger = self._framework_logger

    # -------------------------
    # accessors

    @property
    def client(self) -> WebClient:
        return self._client

    @property
    def installation_store(self) -> Optional[InstallationStore]:
        return self._installation_store

    @property
    def oauth_state_store(self) -> Optional[OAuthStateStore]:
        return self._oauth_state_store

    # -------------------------
    # standalone server

    def start(self, port: int = 3000, path: str = "/slack/events") -> None:
        self.server = SlackAppServer(port=port, path=path, app=self, oauth_flow=self.oauth_flow)
        self.server.start()

    # -------------------------
    # main dispatcher

    # TODO: async_dispatch
    async def async_dispatch(self, req: BoltRequest) -> BoltResponse:
        pass

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
                # run all the middleware attached to this listener first
                resp, next_was_not_called = listener.run_middleware(req=req, resp=resp)
                if next_was_not_called:
                    # The last listener middleware didn't call next() method.
                    # This means the listener is not for this incoming request.
                    continue

                ack = req.context.ack
                starting_time = time.time()
                if self._process_before_response:
                    returned_value = listener(req=req, resp=resp)
                    if isinstance(returned_value, BoltResponse):
                        resp = returned_value
                else:
                    # start the listener function asynchronously
                    self._listener_executor.submit(lambda: listener(req=req, resp=resp))

                    if listener.auto_acknowledgement:
                        # acknowledge immediately in case of Events API
                        ack()
                    else:
                        # await for the completion of ack() in the async listener execution
                        while ack.response is None and time.time() - starting_time <= 3:
                            time.sleep(0.01)

                if self._process_before_response:
                    if ack.response is None and listener.auto_acknowledgement:
                        ack()  # automatic ack() call if the call is not yet done

                    if resp is not None:
                        return resp
                    elif ack.response is not None:
                        return ack.response
                    # None for both means no ack() in the listener
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

    def event(
        self,
        event: Union[str, Pattern, Dict[str, str]],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, Middleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.event(event)
            return self._register_listener(func, primary_matcher, matchers, middleware, True)

        return __call__

    # -------------------------
    # slash commands

    def command(
        self,
        command: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, Middleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.command(command)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # shortcut

    def shortcut(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, Middleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.shortcut(constraints)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    def global_shortcut(
        self,
        callback_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, Middleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.global_shortcut(callback_id)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    def message_shortcut(
        self,
        callback_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, Middleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.message_shortcut(callback_id)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # action

    def action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, Middleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.action(constraints)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    def block_action(
        self,
        action_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, Middleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.block_action(action_id)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # view

    def view(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, Middleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.view(constraints)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # options

    def options(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, Middleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.options(constraints)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    def block_suggestion(
        self,
        action_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, Middleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.block_suggestion(action_id)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    def dialog_suggestion(
        self,
        callback_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, Middleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.dialog_suggestion(callback_id)
            return self._register_listener(func, primary_matcher, matchers, middleware)

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
        middleware: List[Union[Callable, Middleware]],
        auto_acknowledgement: bool = False,
    ) -> Callable[..., None]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        listener_matchers = [CustomListenerMatcher(app_name=self.name, func=f) for f in matchers]
        listener_matchers.insert(0, primary_matcher)
        listener_middleware = []
        for m in middleware:
            if isinstance(m, Middleware):
                listener_middleware.append(m)
            elif isinstance(m, Callable):
                listener_middleware.append(CustomMiddleware(app_name=self.name, func=m))
            else:
                raise ValueError(f"Unexpected value for a listener middleware: {type(m)}")

        self._listeners.append(CustomListener(
            app_name=self.name,
            func=func,
            matchers=listener_matchers,
            middleware=listener_middleware,
            auto_acknowledgement=auto_acknowledgement,
        ))
        return wrapper


# -------------------------

class SlackAppServer:
    def __init__(
        self,
        port: int,
        path: str,
        app: App,
        oauth_flow: Optional[OAuthFlow] = None,
    ):
        self.port = port
        _path = path
        _app = app
        _oauth_flow = oauth_flow

        class SlackAppHandler(SimpleHTTPRequestHandler):

            def do_GET(self):
                if _oauth_flow:
                    _path, _, query = self.path.partition("?")
                    qs = {k: v[0] for k, v in parse_qs(query).items()}
                    if _path == _oauth_flow.install_path:
                        bolt_req = BoltRequest(body="", query=qs, headers=self.headers)
                        bolt_resp = _oauth_flow.handle_installation(bolt_req)
                        self._send_bolt_response(bolt_resp)
                    elif _path == _oauth_flow.redirect_uri_path:
                        bolt_req = BoltRequest(body="", query=qs, headers=self.headers)
                        bolt_resp = _oauth_flow.handle_callback(bolt_req)
                        self._send_bolt_response(bolt_resp)
                    else:
                        self._send_response(404, headers={})
                else:
                    self._send_response(404, headers={})

            def do_POST(self):
                if _path != self.path.split("?")[0]:
                    self._send_response(404, headers={})
                    return

                len_header = self.headers.get("Content-Length") or 0
                content_len = int(len_header)
                request_body = self.rfile.read(content_len).decode("utf-8")
                bolt_req = BoltRequest(body=request_body, headers=self.headers)
                bolt_resp: BoltResponse = _app.dispatch(bolt_req)
                self._send_bolt_response(bolt_resp)

            def _send_bolt_response(self, bolt_resp: BoltResponse):
                self._send_response(
                    status=bolt_resp.status,
                    headers=bolt_resp.headers,
                    body=bolt_resp.body,
                )

            def _send_response(
                self,
                status: int,
                headers: Dict[str, List[str]],
                body: Union[str, dict] = "",
            ):
                self.send_response(status)

                response_body = body if isinstance(body, str) else json.dumps(body)
                body_bytes = response_body.encode("utf-8")

                for k, vs in headers.items():
                    for v in vs:
                        self.send_header(k, v)
                self.send_header("Content-Length", len(body_bytes))
                self.end_headers()
                self.wfile.write(body_bytes)

        self.server = HTTPServer(("0.0.0.0", self.port), SlackAppHandler)

    def start(self):
        print("⚡️ Bolt app is running!")
        try:
            self.server.serve_forever(0.05)
        finally:
            self.server.server_close()
