import asyncio
import inspect
import logging
import os
import time
from asyncio import Future
from typing import Optional, List, Union, Callable, Pattern, Dict, Awaitable

from slack_sdk.oauth import OAuthStateUtils
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.installation_store.async_installation_store import (
    AsyncInstallationStore,
)
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_sdk.oauth.state_store.async_state_store import AsyncOAuthStateStore
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.error import BoltError
from slack_bolt.lazy_listener.async_runner import AsyncLazyListenerRunner
from slack_bolt.lazy_listener.asyncio_runner import AsyncioLazyListenerRunner
from slack_bolt.listener.async_listener import AsyncListener, AsyncCustomListener
from slack_bolt.listener.async_listener_error_handler import (
    AsyncDefaultListenerErrorHandler,
    AsyncListenerErrorHandler,
    AsyncCustomListenerErrorHandler,
)
from slack_bolt.listener_matcher import builtins as builtin_matchers
from slack_bolt.listener_matcher.async_listener_matcher import (
    AsyncListenerMatcher,
    AsyncCustomListenerMatcher,
)
from slack_bolt.logger import get_bolt_logger, get_bolt_app_logger
from slack_bolt.middleware.async_builtins import (
    AsyncSslCheck,
    AsyncRequestVerification,
    AsyncIgnoringSelfEvents,
    AsyncUrlVerification,
)
from slack_bolt.middleware.async_custom_middleware import (
    AsyncMiddleware,
    AsyncCustomMiddleware,
)
from slack_bolt.middleware.async_message_listener_matches import (
    AsyncMessageListenerMatches,
)
from slack_bolt.middleware.authorization.async_multi_teams_authorization import (
    AsyncMultiTeamsAuthorization,
)
from slack_bolt.middleware.authorization.async_single_team_authorization import (
    AsyncSingleTeamAuthorization,
)
from slack_bolt.oauth.async_oauth_flow import AsyncOAuthFlow
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from slack_bolt.util.async_utils import create_async_web_client
from slack_bolt.util.utils import _copy_object


class AsyncApp:
    def __init__(
        self,
        *,
        # Used in logger
        name: Optional[str] = None,
        # Set True when you run this app on a FaaS platform
        process_before_response: bool = False,
        # Basic Information > Credentials > Signing Secret
        signing_secret: Optional[str] = None,
        # for single-workspace apps
        token: Optional[str] = None,
        client: Optional[AsyncWebClient] = None,
        # for multi-workspace apps
        installation_store: Optional[AsyncInstallationStore] = None,
        oauth_state_store: Optional[AsyncOAuthStateStore] = None,
        oauth_state_cookie_name: str = OAuthStateUtils.default_cookie_name,
        oauth_state_expiration_seconds: int = OAuthStateUtils.default_expiration_seconds,
        # for the OAuth flow
        oauth_flow: Optional[AsyncOAuthFlow] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        scopes: Optional[List[str]] = None,
        user_scopes: Optional[List[str]] = None,
        redirect_uri: Optional[str] = None,
        oauth_install_path: Optional[str] = None,
        oauth_redirect_uri_path: Optional[str] = None,
        oauth_success_url: Optional[str] = None,
        oauth_failure_url: Optional[str] = None,
        # No need to set (the value is used only in response to ssl_check requests)
        verification_token: Optional[str] = None,
    ):
        signing_secret = signing_secret or os.environ.get("SLACK_SIGNING_SECRET", None)
        token = token or os.environ.get("SLACK_BOT_TOKEN", None)

        if signing_secret is None or signing_secret == "":
            raise BoltError(
                "Signing secret not found, so could not initialize the Bolt app."
            )

        self._name: str = name or inspect.stack()[1].filename.split(os.path.sep)[-1]
        self._signing_secret: str = signing_secret

        client_id = client_id or os.environ.get("SLACK_CLIENT_ID", None)
        client_secret = client_secret or os.environ.get("SLACK_CLIENT_SECRET", None)
        scopes = scopes or os.environ.get("SLACK_SCOPES", "").split(",")
        user_scopes = user_scopes or os.environ.get("SLACK_USER_SCOPES", "").split(",")
        redirect_uri = redirect_uri or os.environ.get("SLACK_REDIRECT_URI", None)
        oauth_install_path = oauth_install_path or os.environ.get(
            "SLACK_INSTALL_PATH", "/slack/install"
        )
        oauth_redirect_uri_path = oauth_redirect_uri_path or os.environ.get(
            "SLACK_REDIRECT_URI_PATH", "/slack/oauth_redirect"
        )

        self._verification_token: Optional[str] = verification_token or os.environ.get(
            "SLACK_VERIFICATION_TOKEN", None
        )
        self._framework_logger = get_bolt_logger(AsyncApp)

        self._token: Optional[str] = token

        if client is not None:
            if not isinstance(client, AsyncWebClient):
                raise BoltError("client must be an AsyncWebClient")
            self._async_client = client
            self._token = client.token
            if token is not None:
                self._framework_logger.warning(
                    "As you gave client as well, the bot token will be unused."
                )
        else:
            # NOTE: the token here can be None
            self._async_client = create_async_web_client(token)

        self._async_installation_store: Optional[
            AsyncInstallationStore
        ] = installation_store
        self._async_oauth_state_store: Optional[
            AsyncOAuthStateStore
        ] = oauth_state_store

        self._oauth_state_cookie_name = oauth_state_cookie_name
        self._oauth_state_expiration_seconds = oauth_state_expiration_seconds

        self._async_oauth_flow: Optional[AsyncOAuthFlow] = None
        if oauth_flow:
            self._async_oauth_flow = oauth_flow
            if self._async_installation_store is None:
                self._async_installation_store = (
                    self._async_oauth_flow.installation_store
                )
            if self._async_oauth_state_store is None:
                self._async_oauth_state_store = self._async_oauth_flow.oauth_state_store
            if self._async_oauth_flow._async_client is None:
                self._async_oauth_flow._async_client = self._async_client
        else:
            if client_id is not None and client_secret is not None:
                # The OAuth flow support is enabled
                if (
                    self._async_installation_store is None
                    and self._async_oauth_state_store is None
                ):
                    # use the default ones
                    self._async_installation_store = FileInstallationStore(
                        client_id=client_id,
                    )
                    self._async_oauth_state_store = FileOAuthStateStore(
                        expiration_seconds=self._oauth_state_expiration_seconds,
                        client_id=client_id,
                    )

                if (
                    self._async_installation_store is not None
                    and self._async_oauth_state_store is None
                ):
                    raise ValueError(
                        f"Configure an appropriate OAuthStateStore for {self._async_installation_store}"
                    )

                self._async_oauth_flow = AsyncOAuthFlow(
                    client=create_async_web_client(),
                    logger=self._framework_logger,
                    # required storage implementations
                    installation_store=self._async_installation_store,
                    oauth_state_store=self._async_oauth_state_store,
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

        if self._async_installation_store is not None and self._token is not None:
            self._token = None
            self._framework_logger.warning(
                "As you gave installation_store as well, the bot token will be unused."
            )

        self._async_middleware_list: List[Union[Callable, AsyncMiddleware]] = []
        self._async_listeners: List[AsyncListener] = []
        self._async_listener_error_handler = AsyncDefaultListenerErrorHandler(
            logger=self._framework_logger
        )
        self._process_before_response = process_before_response
        self.lazy_listener_runner: AsyncLazyListenerRunner = AsyncioLazyListenerRunner(
            logger=self._framework_logger,
        )

        self._init_middleware_list_done = False
        self._init_async_middleware_list()

    def _init_async_middleware_list(self):
        if self._init_middleware_list_done:
            return
        self._async_middleware_list.append(
            AsyncSslCheck(verification_token=self._verification_token)
        )
        self._async_middleware_list.append(
            AsyncRequestVerification(self._signing_secret)
        )
        if self._async_oauth_flow is None:
            if self._token:
                self._async_middleware_list.append(AsyncSingleTeamAuthorization())
            else:
                raise BoltError(
                    "AsyncOAuthFlow not found, so could not initialize the Bolt app."
                )
        else:
            self._async_middleware_list.append(
                AsyncMultiTeamsAuthorization(self._async_installation_store)
            )

        self._async_middleware_list.append(AsyncIgnoringSelfEvents())
        self._async_middleware_list.append(AsyncUrlVerification())
        self._init_middleware_list_done = True

    # -------------------------
    # accessors

    @property
    def name(self) -> str:
        return self._name

    @property
    def oauth_flow(self) -> Optional[AsyncOAuthFlow]:
        return self._async_oauth_flow

    @property
    def client(self) -> AsyncWebClient:
        return self._async_client

    @property
    def logger(self) -> logging.Logger:
        return self._framework_logger

    @property
    def installation_store(self) -> Optional[AsyncInstallationStore]:
        return self._async_installation_store

    @property
    def oauth_state_store(self) -> Optional[AsyncOAuthStateStore]:
        return self._async_oauth_state_store

    @property
    def listener_error_handler(self) -> AsyncListenerErrorHandler:
        return self._async_listener_error_handler

    # -------------------------
    # standalone server

    def start(self, port: int = 3000, path: str = "/slack/events") -> None:
        from .async_server import AsyncSlackAppServer

        self.server = AsyncSlackAppServer(port=port, path=path, app=self,)
        self.server.start()

    # -------------------------
    # main dispatcher

    async def async_dispatch(self, req: AsyncBoltRequest) -> BoltResponse:
        self._init_context(req)

        resp: BoltResponse = BoltResponse(status=200, body="")
        middleware_state = {"next_called": False}

        async def async_middleware_next():
            middleware_state["next_called"] = True

        for middleware in self._async_middleware_list:
            middleware_state["next_called"] = False
            if self._framework_logger.level <= logging.DEBUG:
                self._framework_logger.debug(f"Applying {middleware.name}")
            resp = await middleware.async_process(
                req=req, resp=resp, next=async_middleware_next
            )
            if not middleware_state["next_called"]:
                return resp

        for listener in self._async_listeners:
            listener_name = listener.ack_function.__name__
            self._framework_logger.debug(f"Checking listener: {listener_name} ...")
            if await listener.async_matches(req=req, resp=resp):
                # run all the middleware attached to this listener first
                resp, next_was_not_called = await listener.run_async_middleware(
                    req=req, resp=resp
                )
                if next_was_not_called:
                    # The last listener middleware didn't call next() method.
                    # This means the listener is not for this incoming request.
                    continue

                self._framework_logger.debug(f"Running listener: {listener_name} ...")
                listener_response: Optional[
                    BoltResponse
                ] = await self.run_async_listener(
                    request=req,
                    response=resp,
                    listener_name=listener_name,
                    async_listener=listener,
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
        async_listener: AsyncListener,
    ) -> Optional[BoltResponse]:
        ack = request.context.ack
        starting_time = time.time()
        if self._process_before_response:
            if not request.lazy_only:
                try:
                    returned_value = await async_listener.run_ack_function(
                        request=request, response=response
                    )
                    if isinstance(returned_value, BoltResponse):
                        response = returned_value
                    if ack.response is None and async_listener.auto_acknowledgement:
                        await ack()  # automatic ack() call if the call is not yet done
                except Exception as e:
                    # The default response status code is 500 in this case.
                    # You can customize this by passing your own error handler.
                    if response is None:
                        response = BoltResponse(status=500)
                    response.status = 500
                    await self._async_listener_error_handler.handle(
                        error=e, request=request, response=response,
                    )
                    ack.response = response

            for lazy_func in async_listener.lazy_functions:
                if request.lazy_function_name:
                    func_name = lazy_func.__name__
                    if func_name == request.lazy_function_name:
                        return await self.lazy_listener_runner.run(
                            function=lazy_func, request=request
                        )
                    else:
                        continue
                else:
                    self._start_lazy_function(lazy_func, request)

            if response is not None:
                self._debug_log_completion(starting_time, response)
                return response
            elif ack.response is not None:
                self._debug_log_completion(starting_time, ack.response)
                return ack.response
        else:
            if async_listener.auto_acknowledgement:
                # acknowledge immediately in case of Events API
                await ack()

            if not request.lazy_only:
                # start the listener function asynchronously
                # NOTE: intentionally
                async def run_ack_function_asynchronously(
                    ack: AsyncAck, request: AsyncBoltRequest, response: BoltResponse,
                ):
                    try:
                        await async_listener.run_ack_function(
                            request=request, response=response
                        )
                    except Exception as e:
                        # The default response status code is 500 in this case.
                        # You can customize this by passing your own error handler.
                        if response is None:
                            response = BoltResponse(status=500)
                        response.status = 500
                        if ack.response is not None:  # already acknowledged
                            response = None

                        await self._async_listener_error_handler.handle(
                            error=e, request=request, response=response,
                        )
                        ack.response = response

                _f: Future = asyncio.ensure_future(
                    run_ack_function_asynchronously(ack, request, response)
                )
                self._framework_logger.debug(
                    f"Async listener: {listener_name} started.."
                )

            for lazy_func in async_listener.lazy_functions:
                if request.lazy_function_name:
                    func_name = lazy_func.__name__
                    if func_name == request.lazy_function_name:
                        return await self.lazy_listener_runner.run(
                            function=lazy_func, request=request
                        )
                    else:
                        continue
                else:
                    self._start_lazy_function(lazy_func, request)

            # await for the completion of ack() in the async listener execution
            while ack.response is None and time.time() - starting_time <= 3:
                await asyncio.sleep(0.01)

            if response is None and ack.response is None:
                self._framework_logger.warning(f"{listener_name} didn't call ack()")
                return None

            if response is None and ack.response is not None:
                response = ack.response
                self._debug_log_completion(starting_time, response)
                return response

            if response is not None:
                return response

        # None for both means no ack() in the listener
        return None

    def _start_lazy_function(
        self, lazy_func: Callable[..., Awaitable[None]], request: AsyncBoltRequest
    ):
        # Start a lazy function asynchronously
        func_name: str = lazy_func.__name__
        self._framework_logger.debug(f"Running lazy listener: {func_name} ...")
        copied_request = self._build_lazy_request(request, func_name)
        self.lazy_listener_runner.start(function=lazy_func, request=copied_request)

    @staticmethod
    def _build_lazy_request(
        request: AsyncBoltRequest, lazy_func_name: str
    ) -> AsyncBoltRequest:
        copied_request = _copy_object(request)
        copied_request.method = "NONE"
        copied_request.lazy_only = True
        copied_request.lazy_function_name = lazy_func_name
        return copied_request

    def _debug_log_completion(
        self, starting_time: float, response: BoltResponse
    ) -> None:
        millis = int((time.time() - starting_time) * 1000)
        self._framework_logger.debug(
            f'Responding with status: {response.status} body: "{response.body}" ({millis} millis)'
        )

    # -------------------------
    # middleware

    def use(self, *args):
        return self.middleware(*args)

    def middleware(self, *args):
        if len(args) > 0:
            func = args[0]
            self._async_middleware_list.append(
                AsyncCustomMiddleware(app_name=self.name, func=func)
            )

    # -------------------------
    # global error handler

    def error(self, *args):
        if len(args) > 0:
            func = args[0]
            self._async_listener_error_handler = AsyncCustomListenerErrorHandler(
                logger=self._framework_logger, func=func,
            )

    # -------------------------
    # events

    def event(
        self,
        event: Union[str, Pattern, Dict[str, str]],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.event(event, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware, True
            )

        return __call__

    def message(
        self,
        keyword: Union[str, Pattern],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        matchers = matchers if matchers else []
        middleware = middleware if middleware else []

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.event("message", True)
            middleware.append(AsyncMessageListenerMatches(keyword))
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware, True
            )

        return __call__

    # -------------------------
    # slash commands

    def command(
        self,
        command: Union[str, Pattern],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.command(command, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    # -------------------------
    # shortcut

    def shortcut(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.shortcut(constraints, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def global_shortcut(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.global_shortcut(callback_id, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def message_shortcut(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.message_shortcut(callback_id, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    # -------------------------
    # action

    def action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.action(constraints, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def block_action(
        self,
        action_id: Union[str, Pattern],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.block_action(action_id, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def attachment_action(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.attachment_action(callback_id, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def dialog_submission(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.dialog_submission(callback_id, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def dialog_cancellation(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.dialog_cancellation(callback_id, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    # -------------------------
    # view

    def view(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.view(constraints, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def view_submission(
        self,
        constraints: Union[str, Pattern],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.view_submission(constraints, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def view_closed(
        self,
        constraints: Union[str, Pattern],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.view_closed(constraints, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    # -------------------------
    # options

    def options(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.options(constraints, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def block_suggestion(
        self,
        action_id: Union[str, Pattern],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.block_suggestion(action_id, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def dialog_suggestion(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[List[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]] = None,
    ):
        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.dialog_suggestion(callback_id, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    # -------------------------

    def _init_context(self, req: AsyncBoltRequest):
        req.context["logger"] = get_bolt_app_logger(self.name)
        req.context["token"] = self._token
        req.context["client"] = self._async_client

    @staticmethod
    def _to_listener_functions(
        kwargs: dict,
    ) -> Optional[List[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        if kwargs:
            functions = [kwargs["ack"]]
            for sub in kwargs["lazy"]:
                functions.append(sub)
            return functions
        return None

    def _register_listener(
        self,
        functions: List[Callable[..., Awaitable[Optional[BoltResponse]]]],
        primary_matcher: AsyncListenerMatcher,
        matchers: Optional[List[Callable[..., Awaitable[bool]]]],
        middleware: Optional[List[Union[Callable, AsyncMiddleware]]],
        auto_acknowledgement: bool = False,
    ) -> None:

        for func in functions:
            if not inspect.iscoroutinefunction(func):
                name = func.__name__
                raise BoltError(
                    f"The listener function ({name}) is not a coroutine function."
                )

        listener_matchers = [
            AsyncCustomListenerMatcher(app_name=self.name, func=f)
            for f in (matchers or [])
        ]
        listener_matchers.insert(0, primary_matcher)
        listener_middleware = []
        for m in middleware or []:
            if isinstance(m, AsyncMiddleware):
                listener_middleware.append(m)
            elif isinstance(m, Callable) and inspect.iscoroutinefunction(m):
                listener_middleware.append(
                    AsyncCustomMiddleware(app_name=self.name, func=m)
                )
            else:
                raise ValueError(
                    f"async function is required for AsyncApp's listener middleware: {type(m)}"
                )

        self._async_listeners.append(
            AsyncCustomListener(
                app_name=self.name,
                ack_function=functions.pop(0),
                lazy_functions=functions,
                matchers=listener_matchers,
                middleware=listener_middleware,
                auto_acknowledgement=auto_acknowledgement,
            )
        )
