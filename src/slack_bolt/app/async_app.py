import asyncio
import inspect
import logging
import os
import re
import time
from asyncio import Future
from functools import wraps
from typing import Optional, List, Union, Callable, Pattern, Dict, Awaitable
from urllib.parse import parse_qs

from aiohttp import web

from slack_bolt.listener_matcher import builtins as builtin_matchers
from slack_bolt.logger import get_bolt_logger, get_bolt_app_logger
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk.oauth import OAuthStateUtils
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.installation_store.async_installation_store import AsyncInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_sdk.oauth.state_store.async_state_store import AsyncOAuthStateStore
from slack_sdk.web.async_client import AsyncWebClient
from ..listener.async_custom_listener import AsyncCustomListener
from ..listener.async_listener import AsyncListener
from ..listener_matcher.async_custom_listener_matcher import AsyncCustomListenerMatcher
from ..listener_matcher.async_listener_matcher import AsyncListenerMatcher
from ..middleware import SslCheck, RequestVerification, IgnoringSelfEvents, UrlVerification
from ..middleware.async_custom_middleware import AsyncCustomMiddleware
from ..middleware.async_middleware import AsyncMiddleware
from ..middleware.authorization.async_multi_teams_authorization import AsyncMultiTeamsAuthorization
from ..middleware.authorization.async_single_team_authorization import AsyncSingleTeamAuthorization
from ..oauth.async_oauth_flow import AsyncOAuthFlow


class AsyncApp():

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
        client: Optional[AsyncWebClient] = None,
        # for multi-workspace apps
        installation_store: Optional[AsyncInstallationStore] = None,
        oauth_state_store: Optional[AsyncOAuthStateStore] = None,
        oauth_state_cookie_name: str = OAuthStateUtils.default_cookie_name,
        oauth_state_expiration_seconds: int = OAuthStateUtils.default_expiration_seconds,

        # for the OAuth flow
        oauth_flow: Optional[AsyncOAuthFlow] = None,
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
        self._framework_logger = get_bolt_logger(AsyncApp)

        self._token: Optional[str] = token

        if client is not None:
            self._client = client
            self._token = client.token
            if token is not None:
                self._framework_logger.warning(
                    "As you gave client as well, the bot token will be unused.")
        else:
            self._client = AsyncWebClient(token=token)  # NOTE: the token here can be None

        self._installation_store: Optional[AsyncInstallationStore] = installation_store
        self._oauth_state_store: Optional[AsyncOAuthStateStore] = oauth_state_store

        self._oauth_state_cookie_name = oauth_state_cookie_name
        self._oauth_state_expiration_seconds = oauth_state_expiration_seconds

        self._oauth_flow: Optional[AsyncOAuthFlow] = None
        if oauth_flow:
            self._oauth_flow = oauth_flow
            if self._installation_store is None:
                self._installation_store = self._oauth_flow.installation_store
            if self._oauth_state_store is None:
                self._oauth_state_store = self._oauth_flow.oauth_state_store
            if self._oauth_flow._client is None:
                self._oauth_flow._client = self._client
        else:
            if client_id is not None and client_secret is not None:
                # The OAuth flow support is enabled
                if self._installation_store is None and self._oauth_state_store is None:
                    # use the default ones
                    self._installation_store = FileInstallationStore(
                        client_id=client_id,
                    )
                    self._oauth_state_store = FileOAuthStateStore(
                        expiration_seconds=self._oauth_state_expiration_seconds,
                        client_id=client_id,
                    )

                if self._installation_store is not None and self._oauth_state_store is None:
                    raise ValueError(f"Configure an appropriate OAuthStateStore for {self._installation_store}")

                self._oauth_flow = AsyncOAuthFlow(
                    client=AsyncWebClient(token=None),
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

        self._middleware_list: List[Union[Callable, AsyncMiddleware]] = []
        self._listeners: List[AsyncListener] = []
        self._process_before_response = process_before_response

        self._listener_tasks = []

        self._init_middleware_list_done = False
        self._init_middleware_list()
        self._init_listeners_done = False
        self._init_listeners()

    def _init_middleware_list(self):
        if self._init_middleware_list_done:
            return
        self._middleware_list.append(SslCheck(verification_token=self._verification_token))
        self._middleware_list.append(RequestVerification(self._signing_secret))
        if self._oauth_flow is None and self._token:
            self._middleware_list.append(AsyncSingleTeamAuthorization())
        else:
            self._middleware_list.append(AsyncMultiTeamsAuthorization(self._installation_store))
        self._middleware_list.append(IgnoringSelfEvents())
        self._middleware_list.append(UrlVerification())
        self._init_middleware_list_done = True

    def _init_listeners(self):
        if self._init_listeners_done:
            return
        self._init_listeners_done = True

    # -------------------------
    # accessors

    @property
    def oauth_flow(self) -> Optional[AsyncOAuthFlow]:
        return self._oauth_flow

    @property
    def client(self) -> AsyncWebClient:
        return self._client

    @property
    def installation_store(self) -> Optional[AsyncInstallationStore]:
        return self._installation_store

    @property
    def oauth_state_store(self) -> Optional[AsyncOAuthStateStore]:
        return self._oauth_state_store

    # -------------------------
    # standalone server

    def start(self, port: int = 3000, path: str = "/slack/events") -> None:
        self.server = AsyncSlackAppServer(
            port=port,
            path=path,
            app=self,
        )
        self.server.start()

    # -------------------------
    # main dispatcher

    async def async_dispatch(self, req: AsyncBoltRequest) -> BoltResponse:
        self._init_context(req)

        resp: BoltResponse = BoltResponse(status=200, body=None)
        middleware_state = {"next_called": False}

        async def middleware_next():
            middleware_state["next_called"] = True

        for middleware in self._middleware_list:
            middleware_state["next_called"] = False
            if self._framework_logger.level <= logging.DEBUG:
                self._framework_logger.debug(f"Applying {middleware.name}")
            resp = await middleware.async_process(req=req, resp=resp, next=middleware_next)
            if not middleware_state["next_called"]:
                return resp

        for listener in self._listeners:
            if await listener.async_matches(req=req, resp=resp):
                listener_name = listener.func.__name__
                # run all the middleware attached to this listener first
                resp, next_was_not_called = await listener.run_async_middleware(req=req, resp=resp)
                if next_was_not_called:
                    # The last listener middleware didn't call next() method.
                    # This means the listener is not for this incoming request.
                    continue

                self._framework_logger.debug(f"Starting listener: {listener_name}")
                listener_response: Optional[BoltResponse] = await self.run_async_listener(
                    request=req,
                    response=resp,
                    listener_name=listener_name,
                    listener=listener,
                )
                if listener_response is not None:
                    return listener_response

        self._framework_logger.warning(f"Unhandled request ({req.payload})")
        return BoltResponse(status=404, body={"error": "unhandled request"})

    async def run_async_listener(
        self,
        request: AsyncBoltRequest,
        response: BoltResponse,
        listener_name: str,
        listener: AsyncListener,
    ) -> Optional[BoltResponse]:
        ack = request.context.ack
        starting_time = time.time()
        if self._process_before_response:
            returned_value = await listener(req=request, resp=response)
            if isinstance(returned_value, BoltResponse):
                response = returned_value
            if ack.response is None and listener.auto_acknowledgement:
                await ack()  # automatic ack() call if the call is not yet done

            if response is not None:
                return response
            elif ack.response is not None:
                return ack.response
        else:
            if listener.auto_acknowledgement:
                # acknowledge immediately in case of Events API
                await ack()

            # start the listener function asynchronously
            # NOTE: intentionally
            future: Future = asyncio.ensure_future(listener(req=request, resp=response))
            self._framework_logger.debug(f"Async execution of listener: {listener_name} started...")

            # await for the completion of ack() in the async listener execution
            while ack.response is None and time.time() - starting_time <= 3:
                await asyncio.sleep(0.01)

            if ack.response is not None:
                response = ack.response
                millis = int((time.time() - starting_time) * 1000)
                self._framework_logger.debug(
                    f"Responding with status: {response.status} body: \"{response.body}\" ({millis} millis)")
                return response
            else:
                self._framework_logger.warning(f"{listener_name} didn't call ack()")

        # None for both means no ack() in the listener
        return None

    # -------------------------
    # middleware

    def use(self, *args):
        return self.middleware(*args)

    def middleware(self, *args):
        if len(args) > 0:
            func = args[0]
            self._middleware_list.append(AsyncCustomMiddleware(app_name=self.name, func=func))

    # -------------------------
    # events

    def event(
        self,
        event: Union[str, Pattern, Dict[str, str]],
        matchers: List[Callable[..., Awaitable[bool]]] = [],
        middleware: List[Union[Callable, AsyncMiddleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.event(event, True)
            return self._register_listener(func, primary_matcher, matchers, middleware, True)

        return __call__

    # -------------------------
    # slash commands

    def command(
        self,
        command: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, AsyncMiddleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.command(command, True)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # shortcut

    def shortcut(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, AsyncMiddleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.shortcut(constraints, True)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    def global_shortcut(
        self,
        callback_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, AsyncMiddleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.global_shortcut(callback_id, True)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    def message_shortcut(
        self,
        callback_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, AsyncMiddleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.message_shortcut(callback_id, True)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # action

    def action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, AsyncMiddleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.action(constraints, True)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    def block_action(
        self,
        action_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, AsyncMiddleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.block_action(action_id, True)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # view

    def view(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, AsyncMiddleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.view(constraints, True)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # options

    def options(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, AsyncMiddleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.options(constraints, True)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    def block_suggestion(
        self,
        action_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, AsyncMiddleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.block_suggestion(action_id, True)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    def dialog_suggestion(
        self,
        callback_id: Union[str, Pattern],
        matchers: List[Callable[..., bool]] = [],
        middleware: List[Union[Callable, AsyncMiddleware]] = [],
    ):
        def __call__(func):
            primary_matcher = builtin_matchers.dialog_suggestion(callback_id, True)
            return self._register_listener(func, primary_matcher, matchers, middleware)

        return __call__

    # -------------------------

    def _init_context(self, req: AsyncBoltRequest):
        req.context["logger"] = get_bolt_app_logger(self.name)
        req.context["token"] = self._token
        req.context["client"] = self._client

    def _register_listener(
        self,
        func,
        primary_matcher: AsyncListenerMatcher,
        matchers: List[Callable[..., Awaitable[bool]]],
        middleware: List[Union[Callable, AsyncMiddleware]],
        auto_acknowledgement: bool = False,
    ) -> Callable[..., None]:

        if not inspect.iscoroutinefunction(func):
            raise ValueError(f"async function is required for AsyncApp's listener: {type(func)}")

        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        listener_matchers = [AsyncCustomListenerMatcher(app_name=self.name, func=f) for f in matchers]
        listener_matchers.insert(0, primary_matcher)
        listener_middleware = []
        for m in middleware:
            if isinstance(m, AsyncMiddleware):
                listener_middleware.append(m)
            elif isinstance(m, Callable) and inspect.iscoroutinefunction(m):
                listener_middleware.append(AsyncCustomMiddleware(app_name=self.name, func=m))
            else:
                raise ValueError(f"async function is required for AsyncApp's listener middleware: {type(m)}")

        self._listeners.append(AsyncCustomListener(
            app_name=self.name,
            func=func,
            matchers=listener_matchers,
            middleware=listener_middleware,
            auto_acknowledgement=auto_acknowledgement,
        ))
        return wrapper


# -------------------------

def to_aiohttp_response(bolt_resp: BoltResponse) -> web.Response:
    content_type = bolt_resp.headers.pop(
        "content-type",
        ["application/json" if bolt_resp.body.startswith("{") else "text/plain"]
    )[0]
    content_type = re.sub(";\s*charset=utf-8", "", content_type)
    resp = web.Response(
        status=bolt_resp.status,
        body=bolt_resp.body,
        headers=bolt_resp.first_headers_without_set_cookie(),
        content_type=content_type,
    )
    for cookie in bolt_resp.cookies():
        for name, c in cookie.items():
            resp.set_cookie(
                name=name,
                value=c.value,
                max_age=c.get("max-age", None),
                expires=c.get("expires", None),
                path=c.get("path", None),
                domain=c.get("domain", None),
                secure=True,
                httponly=True,
            )
    return resp


class AsyncSlackAppServer:

    def __init__(
        self,
        port: int,
        path: str,
        app: AsyncApp,
    ):
        self.port = port
        self.app = app
        self.path = path

        self.web_app = web.Application()
        oauth_flow = self.app.oauth_flow
        if oauth_flow:
            self.web_app.add_routes([
                web.get(oauth_flow.install_path, self.handle_get_requests),
                web.get(oauth_flow.redirect_uri_path, self.handle_get_requests),
                web.post(self.path, self.handle_post_requests)
            ])
        else:
            self.web_app.add_routes([
                web.post(self.path, self.handle_post_requests)
            ])

    async def handle_get_requests(self, request: web.Request) -> web.Response:
        oauth_flow = self.app.oauth_flow
        if oauth_flow:
            _path, query = request.path, request.query_string
            qs = {k: v[0] for k, v in parse_qs(query).items()}
            if _path == self.app.oauth_flow.install_path:
                bolt_req = AsyncBoltRequest(body="", query=qs, headers=request.headers)
                bolt_resp = await oauth_flow.handle_installation(bolt_req)
                return to_aiohttp_response(bolt_resp)
            elif _path == oauth_flow.redirect_uri_path:
                bolt_req = AsyncBoltRequest(body="", query=qs, headers=request.headers)
                bolt_resp = await oauth_flow.handle_callback(bolt_req)
                return to_aiohttp_response(bolt_resp)
            else:
                return web.Response(status=404)
        else:
            return web.Response(status=404)

    async def handle_post_requests(self, request: web.Request) -> web.Response:
        if self.path != request.path:
            return web.Response(status=404)

        request_body = await request.text()
        bolt_req = AsyncBoltRequest(body=request_body, headers=request.headers)
        bolt_resp: BoltResponse = await self.app.async_dispatch(bolt_req)
        return to_aiohttp_response(bolt_resp)

    def start(self):
        print("⚡️ Bolt app is running!")
        web.run_app(self.web_app, host="0.0.0.0", port=self.port)
