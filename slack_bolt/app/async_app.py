import inspect
import logging
import os
import time
from typing import Optional, List, Union, Callable, Pattern, Dict, Awaitable, Sequence, Any
import warnings

from aiohttp import web

from slack_bolt.app.async_server import AsyncSlackAppServer
from slack_bolt.context.assistant.async_assistant_utilities import AsyncAssistantUtilities
from slack_bolt.context.assistant.thread_context_store.async_store import (
    AsyncAssistantThreadContextStore,
)
from slack_bolt.listener.async_builtins import AsyncTokenRevocationListeners
from slack_bolt.listener.async_listener_start_handler import (
    AsyncDefaultListenerStartHandler,
)
from slack_bolt.listener.async_listener_completion_handler import (
    AsyncDefaultListenerCompletionHandler,
)
from slack_bolt.listener.asyncio_runner import AsyncioListenerRunner
from slack_bolt.middleware.assistant.async_assistant import AsyncAssistant
from slack_bolt.middleware.async_middleware_error_handler import (
    AsyncCustomMiddlewareErrorHandler,
    AsyncDefaultMiddlewareErrorHandler,
    AsyncMiddlewareErrorHandler,
)
from slack_bolt.middleware.message_listener_matches.async_message_listener_matches import (
    AsyncMessageListenerMatches,
)
from slack_bolt.oauth.async_internals import select_consistent_installation_store
from slack_bolt.request.payload_utils import is_assistant_event, to_event
from slack_bolt.util.utils import get_name_for_callable, is_callable_coroutine
from slack_bolt.workflows.step.async_step import (
    AsyncWorkflowStep,
    AsyncWorkflowStepBuilder,
)
from slack_bolt.workflows.step.async_step_middleware import AsyncWorkflowStepMiddleware
from slack_sdk.oauth.installation_store.async_installation_store import (
    AsyncInstallationStore,
)
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.authorization import AuthorizeResult
from slack_bolt.authorization.async_authorize import (
    AsyncAuthorize,
    AsyncCallableAuthorize,
    AsyncInstallationStoreAuthorize,
)
from slack_bolt.error import BoltError, BoltUnhandledRequestError
from slack_bolt.logger.messages import (
    error_oauth_flow_or_authorize_required,
    warning_client_prioritized_and_token_skipped,
    warning_token_skipped,
    error_token_required,
    warning_unhandled_request,
    debug_checking_listener,
    debug_running_listener,
    error_unexpected_listener_middleware,
    error_listener_function_must_be_coro_func,
    error_client_invalid_type_async,
    error_authorize_conflicts,
    error_oauth_settings_invalid_type_async,
    error_oauth_flow_invalid_type_async,
    warning_bot_only_conflicts,
    debug_return_listener_middleware_response,
    info_default_oauth_settings_loaded,
    error_installation_store_required_for_builtin_listeners,
    warning_unhandled_by_global_middleware,
    warning_ack_timeout_has_no_effect,
)
from slack_bolt.lazy_listener.asyncio_runner import AsyncioLazyListenerRunner
from slack_bolt.listener.async_listener import AsyncListener, AsyncCustomListener
from slack_bolt.listener.async_listener_error_handler import (
    AsyncDefaultListenerErrorHandler,
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
    AsyncAttachingFunctionToken,
)
from slack_bolt.middleware.async_custom_middleware import (
    AsyncMiddleware,
    AsyncCustomMiddleware,
)
from slack_bolt.middleware.authorization.async_multi_teams_authorization import (
    AsyncMultiTeamsAuthorization,
)
from slack_bolt.middleware.authorization.async_single_team_authorization import (
    AsyncSingleTeamAuthorization,
)
from slack_bolt.oauth.async_oauth_flow import AsyncOAuthFlow
from slack_bolt.oauth.async_oauth_settings import AsyncOAuthSettings
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from slack_bolt.util.async_utils import create_async_web_client


class AsyncApp:
    def __init__(
        self,
        *,
        logger: Optional[logging.Logger] = None,
        # Used in logger
        name: Optional[str] = None,
        # Set True when you run this app on a FaaS platform
        process_before_response: bool = False,
        # Set True if you want to handle an unhandled request as an exception
        raise_error_for_unhandled_request: bool = False,
        # Basic Information > Credentials > Signing Secret
        signing_secret: Optional[str] = None,
        # for single-workspace apps
        token: Optional[str] = None,
        client: Optional[AsyncWebClient] = None,
        # for multi-workspace apps
        before_authorize: Optional[Union[AsyncMiddleware, Callable[..., Awaitable[Any]]]] = None,
        authorize: Optional[Callable[..., Awaitable[AuthorizeResult]]] = None,
        user_facing_authorize_error_message: Optional[str] = None,
        installation_store: Optional[AsyncInstallationStore] = None,
        # for either only bot scope usage or v1.0.x compatibility
        installation_store_bot_only: Optional[bool] = None,
        # for customizing the built-in middleware
        request_verification_enabled: bool = True,
        ignoring_self_events_enabled: bool = True,
        ignoring_self_assistant_message_events_enabled: bool = True,
        ssl_check_enabled: bool = True,
        url_verification_enabled: bool = True,
        attaching_function_token_enabled: bool = True,
        # for the OAuth flow
        oauth_settings: Optional[AsyncOAuthSettings] = None,
        oauth_flow: Optional[AsyncOAuthFlow] = None,
        # No need to set (the value is used only in response to ssl_check requests)
        verification_token: Optional[str] = None,
        # for AI Agents & Assistants
        assistant_thread_context_store: Optional[AsyncAssistantThreadContextStore] = None,
    ):
        """Bolt App that provides functionalities to register middleware/listeners.

            import os
            from slack_bolt.async_app import AsyncApp

            # Initializes your app with your bot token and signing secret
            app = AsyncApp(
                token=os.environ.get("SLACK_BOT_TOKEN"),
                signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
            )

            # Listens to incoming messages that contain "hello"
            @app.message("hello")
            async def message_hello(message, say):  # async function
                # say() sends a message to the channel where the event was triggered
                await say(f"Hey there <@{message['user']}>!")

            # Start your app
            if __name__ == "__main__":
                app.start(port=int(os.environ.get("PORT", 3000)))

        Refer to https://docs.slack.dev/tools/bolt-python/concepts/async for details.

        If you would like to build an OAuth app for enabling the app to run with multiple workspaces,
        refer to https://docs.slack.dev/tools/bolt-python/concepts/authenticating-oauth to learn how to configure the app.

        Args:
            logger: The custom logger that can be used in this app.
            name: The application name that will be used in logging. If absent, the source file name will be used.
            process_before_response: True if this app runs on Function as a Service. (Default: False)
            raise_error_for_unhandled_request: True if you want to raise exceptions for unhandled requests
                and use @app.error listeners instead of
                the built-in handler, which pints warning logs and returns 404 to Slack (Default: False)
            signing_secret: The Signing Secret value used for verifying requests from Slack.
            token: The bot/user access token required only for single-workspace app.
            client: The singleton `slack_sdk.web.async_client.AsyncWebClient` instance for this app.
            before_authorize: A global middleware that can be executed right before authorize function
            authorize: The function to authorize an incoming request from Slack
                by checking if there is a team/user in the installation data.
            user_facing_authorize_error_message: The user-facing error message to display
                when the app is installed but the installation is not managed by this app's installation store
            installation_store: The module offering save/find operations of installation data
            installation_store_bot_only: Use `AsyncInstallationStore#async_find_bot()` if True (Default: False)
            request_verification_enabled: False if you would like to disable the built-in middleware (Default: True).
                `AsyncRequestVerification` is a built-in middleware that verifies the signature in HTTP Mode requests.
                Make sure if it's safe enough when you turn a built-in middleware off.
                We strongly recommend using RequestVerification for better security.
                If you have a proxy that verifies request signature in front of the Bolt app,
                it's totally fine to disable RequestVerification to avoid duplication of work.
                Don't turn it off just for easiness of development.
            ignoring_self_events_enabled: False if you would like to disable the built-in middleware (Default: True).
                `AsyncIgnoringSelfEvents` is a built-in middleware that enables Bolt apps to easily skip the events
                generated by this app's bot user (this is useful for avoiding code error causing an infinite loop).
            ignoring_self_assistant_message_events_enabled: False if you would like to disable the built-in middleware.
                `IgnoringSelfEvents` for this app's bot user message events within an assistant thread
                This is useful for avoiding code error causing an infinite loop; Default: True
            url_verification_enabled: False if you would like to disable the built-in middleware (Default: True).
                `AsyncUrlVerification` is a built-in middleware that handles url_verification requests
                that verify the endpoint for Events API in HTTP Mode requests.
            ssl_check_enabled: bool = False if you would like to disable the built-in middleware (Default: True).
                `AsyncSslCheck` is a built-in middleware that handles ssl_check requests from Slack.
            attaching_function_token_enabled: False if you would like to disable the built-in middleware (Default: True).
                `AsyncAttachingFunctionToken` is a built-in middleware that injects the just-in-time workflow-execution token
                when your app receives `function_executed` or interactivity events scoped to a custom step.
            oauth_settings: The settings related to Slack app installation flow (OAuth flow)
            oauth_flow: Instantiated `slack_bolt.oauth.AsyncOAuthFlow`. This is always prioritized over oauth_settings.
            verification_token: Deprecated verification mechanism. This can be used only for ssl_check requests.
            assistant_thread_context_store: Custom AssistantThreadContext store (Default: the built-in implementation,
                which uses a parent message's metadata to store the latest context)
        """
        if signing_secret is None:
            signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "")
        token = token or os.environ.get("SLACK_BOT_TOKEN")

        self._name: str = name or inspect.stack()[1].filename.split(os.path.sep)[-1]
        self._signing_secret: str = signing_secret
        self._verification_token: Optional[str] = verification_token or os.environ.get("SLACK_VERIFICATION_TOKEN", None)
        # If a logger is explicitly passed when initializing, the logger works as the base logger.
        # The base logger's logging settings will be propagated to all the loggers created by bolt-python.
        self._base_logger = logger
        # The framework logger is supposed to be used for the internal logging.
        # Also, it's accessible via `app.logger` as the app's singleton logger.
        self._framework_logger = logger or get_bolt_logger(AsyncApp)
        self._raise_error_for_unhandled_request = raise_error_for_unhandled_request

        self._token: Optional[str] = token

        if client is not None:
            if not isinstance(client, AsyncWebClient):
                raise BoltError(error_client_invalid_type_async())
            self._async_client = client
            self._token = client.token
            if token is not None:
                self._framework_logger.warning(warning_client_prioritized_and_token_skipped())
        else:
            self._async_client = create_async_web_client(
                # NOTE: the token here can be None
                token=token,
                logger=self._framework_logger,
            )

        # --------------------------------------
        # Authorize & OAuthFlow initialization
        # --------------------------------------

        self._async_before_authorize: Optional[AsyncMiddleware] = None
        if before_authorize is not None:
            if callable(before_authorize):
                self._async_before_authorize = AsyncCustomMiddleware(
                    app_name=self._name,
                    func=before_authorize,
                    base_logger=self._framework_logger,
                )
            elif isinstance(before_authorize, AsyncMiddleware):
                self._async_before_authorize = before_authorize

        self._async_authorize: Optional[AsyncAuthorize] = None
        if authorize is not None:
            if isinstance(authorize, AsyncAuthorize):
                # As long as an advanced developer understands what they're doing,
                # bolt-python should not prevent customizing authorize middleware
                self._async_authorize = authorize
            else:
                if oauth_settings is not None or oauth_flow is not None:
                    # If the given authorize is a simple function,
                    # it does not work along with installation_store.
                    raise BoltError(error_authorize_conflicts())
                self._async_authorize = AsyncCallableAuthorize(logger=self._framework_logger, func=authorize)

        self._async_installation_store: Optional[AsyncInstallationStore] = installation_store
        if self._async_installation_store is not None and self._async_authorize is None:
            settings = oauth_flow.settings if oauth_flow is not None else oauth_settings
            self._async_authorize = AsyncInstallationStoreAuthorize(
                installation_store=self._async_installation_store,
                client_id=settings.client_id if settings is not None else None,
                client_secret=settings.client_secret if settings is not None else None,
                logger=self._framework_logger,
                bot_only=installation_store_bot_only or False,
                client=self._async_client,  # for proxy use cases etc.
                user_token_resolution=(settings.user_token_resolution if settings is not None else "authed_user"),
            )

        self._async_oauth_flow: Optional[AsyncOAuthFlow] = None

        if (
            oauth_settings is None
            and os.environ.get("SLACK_CLIENT_ID") is not None
            and os.environ.get("SLACK_CLIENT_SECRET") is not None
        ):
            # initialize with the default settings
            oauth_settings = AsyncOAuthSettings()

            if oauth_flow is None and installation_store is None:
                # show info-level log for avoiding confusions
                self._framework_logger.info(info_default_oauth_settings_loaded())

        if oauth_flow:
            if not isinstance(oauth_flow, AsyncOAuthFlow):
                raise BoltError(error_oauth_flow_invalid_type_async())

            self._async_oauth_flow = oauth_flow
            installation_store = select_consistent_installation_store(
                client_id=self._async_oauth_flow.client_id,
                app_store=self._async_installation_store,
                oauth_flow_store=self._async_oauth_flow.settings.installation_store,
                logger=self._framework_logger,
            )
            self._async_installation_store = installation_store
            if installation_store is not None:
                self._async_oauth_flow.settings.installation_store = installation_store

            if self._async_oauth_flow._async_client is None:
                self._async_oauth_flow._async_client = self._async_client
            if self._async_authorize is None:
                self._async_authorize = self._async_oauth_flow.settings.authorize
        elif oauth_settings is not None:
            if not isinstance(oauth_settings, AsyncOAuthSettings):
                raise BoltError(error_oauth_settings_invalid_type_async())

            installation_store = select_consistent_installation_store(
                client_id=oauth_settings.client_id,
                app_store=self._async_installation_store,
                oauth_flow_store=oauth_settings.installation_store,
                logger=self._framework_logger,
            )
            self._async_installation_store = installation_store
            if installation_store is not None:
                oauth_settings.installation_store = installation_store

            self._async_oauth_flow = AsyncOAuthFlow(client=self._async_client, logger=self.logger, settings=oauth_settings)
            if self._async_authorize is None:
                self._async_authorize = self._async_oauth_flow.settings.authorize
            self._async_authorize.token_rotation_expiration_minutes = oauth_settings.token_rotation_expiration_minutes  # type: ignore[attr-defined] # noqa: E501

        if (self._async_installation_store is not None or self._async_authorize is not None) and self._token is not None:
            self._token = None
            self._framework_logger.warning(warning_token_skipped())

        # after setting bot_only here, __init__ cannot replace authorize function
        if installation_store_bot_only is not None and self._async_oauth_flow is not None:
            app_bot_only = installation_store_bot_only or False
            oauth_flow_bot_only = self._async_oauth_flow.settings.installation_store_bot_only
            if app_bot_only != oauth_flow_bot_only:
                self.logger.warning(warning_bot_only_conflicts())
                self._async_oauth_flow.settings.installation_store_bot_only = app_bot_only
                self._async_authorize.bot_only = app_bot_only  # type: ignore[union-attr]

        self._async_tokens_revocation_listeners: Optional[AsyncTokenRevocationListeners] = None
        if self._async_installation_store is not None:
            self._async_tokens_revocation_listeners = AsyncTokenRevocationListeners(self._async_installation_store)

        # --------------------------------------
        # Middleware Initialization
        # --------------------------------------

        self._async_middleware_list: List[AsyncMiddleware] = []
        self._async_listeners: List[AsyncListener] = []

        self._assistant_thread_context_store = assistant_thread_context_store

        self._process_before_response = process_before_response
        self._async_listener_runner = AsyncioListenerRunner(
            logger=self._framework_logger,
            process_before_response=process_before_response,
            listener_error_handler=AsyncDefaultListenerErrorHandler(logger=self._framework_logger),
            listener_start_handler=AsyncDefaultListenerStartHandler(logger=self._framework_logger),
            listener_completion_handler=AsyncDefaultListenerCompletionHandler(logger=self._framework_logger),
            lazy_listener_runner=AsyncioLazyListenerRunner(
                logger=self._framework_logger,
            ),
        )
        self._async_middleware_error_handler: AsyncMiddlewareErrorHandler = AsyncDefaultMiddlewareErrorHandler(
            logger=self._framework_logger,
        )

        self._init_middleware_list_done = False
        self._init_async_middleware_list(
            request_verification_enabled=request_verification_enabled,
            ignoring_self_events_enabled=ignoring_self_events_enabled,
            ignoring_self_assistant_message_events_enabled=ignoring_self_assistant_message_events_enabled,
            ssl_check_enabled=ssl_check_enabled,
            url_verification_enabled=url_verification_enabled,
            attaching_function_token_enabled=attaching_function_token_enabled,
            user_facing_authorize_error_message=user_facing_authorize_error_message,
        )

        self._server: Optional[AsyncSlackAppServer] = None

    def _init_async_middleware_list(
        self,
        request_verification_enabled: bool = True,
        ignoring_self_events_enabled: bool = True,
        ignoring_self_assistant_message_events_enabled: bool = True,
        ssl_check_enabled: bool = True,
        url_verification_enabled: bool = True,
        attaching_function_token_enabled: bool = True,
        user_facing_authorize_error_message: Optional[str] = None,
    ):
        if self._init_middleware_list_done:
            return
        if ssl_check_enabled is True:
            self._async_middleware_list.append(
                AsyncSslCheck(
                    verification_token=self._verification_token,
                    base_logger=self._base_logger,
                )
            )
        if request_verification_enabled is True:
            self._async_middleware_list.append(AsyncRequestVerification(self._signing_secret, base_logger=self._base_logger))

        if self._async_before_authorize is not None:
            self._async_middleware_list.append(self._async_before_authorize)

        # As authorize is required for making a Bolt app function, we don't offer the flag to disable this
        if self._async_oauth_flow is None:
            if self._token:
                self._async_middleware_list.append(
                    AsyncSingleTeamAuthorization(
                        base_logger=self._base_logger,
                        user_facing_authorize_error_message=user_facing_authorize_error_message,
                    )
                )
            elif self._async_authorize is not None:
                self._async_middleware_list.append(
                    AsyncMultiTeamsAuthorization(
                        authorize=self._async_authorize,
                        base_logger=self._base_logger,
                        user_facing_authorize_error_message=user_facing_authorize_error_message,
                    )
                )
            else:
                raise BoltError(error_token_required())
        elif self._async_authorize is not None:
            self._async_middleware_list.append(
                AsyncMultiTeamsAuthorization(
                    authorize=self._async_authorize,
                    base_logger=self._base_logger,
                    user_token_resolution=self._async_oauth_flow.settings.user_token_resolution,
                    user_facing_authorize_error_message=user_facing_authorize_error_message,
                )
            )
        else:
            raise BoltError(error_oauth_flow_or_authorize_required())

        if ignoring_self_events_enabled is True:
            self._async_middleware_list.append(
                AsyncIgnoringSelfEvents(
                    base_logger=self._base_logger,
                    ignoring_self_assistant_message_events_enabled=ignoring_self_assistant_message_events_enabled,
                )
            )
        if url_verification_enabled is True:
            self._async_middleware_list.append(AsyncUrlVerification(base_logger=self._base_logger))
        if attaching_function_token_enabled is True:
            self._async_middleware_list.append(AsyncAttachingFunctionToken())
        self._init_middleware_list_done = True

    # -------------------------
    # accessors

    @property
    def name(self) -> str:
        """The name of this app (default: the filename)"""
        return self._name

    @property
    def oauth_flow(self) -> Optional[AsyncOAuthFlow]:
        """Configured `OAuthFlow` object if exists."""
        return self._async_oauth_flow

    @property
    def client(self) -> AsyncWebClient:
        """The singleton `slack_sdk.web.async_client.AsyncWebClient` instance in this app."""
        return self._async_client

    @property
    def logger(self) -> logging.Logger:
        """The logger this app uses."""
        return self._framework_logger

    @property
    def installation_store(self) -> Optional[AsyncInstallationStore]:
        """The `slack_sdk.oauth.AsyncInstallationStore` that can be used in the `authorize` middleware."""
        return self._async_installation_store

    @property
    def listener_runner(self) -> AsyncioListenerRunner:
        """The asyncio-based executor for asynchronously running listeners."""
        return self._async_listener_runner

    @property
    def process_before_response(self) -> bool:
        return self._process_before_response or False

    # -------------------------
    # standalone server

    from .async_server import AsyncSlackAppServer

    def server(
        self,
        port: int = 3000,
        path: str = "/slack/events",
        host: Optional[str] = None,
    ) -> AsyncSlackAppServer:
        """Configure a web server using AIOHTTP.
        Refer to https://docs.aiohttp.org/ for more details about AIOHTTP.

        Args:
            port: The port to listen on (Default: 3000)
            path: The path to handle request from Slack (Default: `/slack/events`)
            host: The hostname to serve the web endpoints. (Default: 0.0.0.0)
        """
        if self._server is None or self._server.port != port or self._server.path != path:
            self._server = AsyncSlackAppServer(
                port=port,
                path=path,
                app=self,
                host=host,
            )
        return self._server

    def web_app(self, path: str = "/slack/events", port: int = 3000) -> web.Application:
        """Returns a `web.Application` instance for aiohttp-devtools users.

            from slack_bolt.async_app import AsyncApp
            app = AsyncApp()

            @app.event("app_mention")
            async def event_test(body, say, logger):
                logger.info(body)
                await say("What's up?")

            def app_factory():
                return app.web_app()

            # adev runserver --port 3000 --app-factory app_factory async_app.py

        Args:
            path: The path to receive incoming requests from Slack
            port: The port to listen on (Default: 3000)
        """
        return self.server(path=path, port=port).web_app

    def start(self, port: int = 3000, path: str = "/slack/events", host: Optional[str] = None) -> None:
        """Start a web server using AIOHTTP.
        Refer to https://docs.aiohttp.org/ for more details about AIOHTTP.

        Args:
            port: The port to listen on (Default: 3000)
            path: The path to handle request from Slack (Default: `/slack/events`)
            host: The hostname to serve the web endpoints. (Default: 0.0.0.0)
        """
        self.server(port=port, path=path, host=host).start()

    # -------------------------
    # main dispatcher

    async def async_dispatch(self, req: AsyncBoltRequest) -> BoltResponse:
        """Applies all middleware and dispatches an incoming request from Slack to the right code path.

        Args:
            req: An incoming request from Slack.

        Returns:
            The response generated by this Bolt app.
        """
        starting_time = time.time()
        self._init_context(req)

        resp: Optional[BoltResponse] = BoltResponse(status=200, body="")
        middleware_state = {"next_called": False}

        async def async_middleware_next():
            middleware_state["next_called"] = True

        try:
            for middleware in self._async_middleware_list:
                middleware_state["next_called"] = False
                if self._framework_logger.level <= logging.DEBUG:
                    self._framework_logger.debug(f"Applying {middleware.name}")
                resp = await middleware.async_process(
                    req=req, resp=resp, next=async_middleware_next  # type: ignore[arg-type]
                )
                if not middleware_state["next_called"]:
                    if resp is None:
                        # next() method was not called without providing the response to return to Slack
                        # This should not be an intentional handling in usual use cases.
                        resp = BoltResponse(status=404, body={"error": "no next() calls in middleware"})
                        if self._raise_error_for_unhandled_request is True:
                            try:
                                raise BoltUnhandledRequestError(
                                    request=req,
                                    current_response=resp,
                                    last_global_middleware_name=middleware.name,
                                )
                            except BoltUnhandledRequestError as e:
                                await self._async_listener_runner.listener_error_handler.handle(
                                    error=e,
                                    request=req,
                                    response=resp,
                                )
                            return resp
                        self._framework_logger.warning(warning_unhandled_by_global_middleware(middleware.name, req))
                        return resp
                    return resp

            for listener in self._async_listeners:
                listener_name = get_name_for_callable(listener.ack_function)
                self._framework_logger.debug(debug_checking_listener(listener_name))
                if await listener.async_matches(req=req, resp=resp):  # type: ignore[arg-type]
                    # run all the middleware attached to this listener first
                    (middleware_resp, next_was_not_called) = await listener.run_async_middleware(
                        req=req, resp=resp  # type: ignore[arg-type]
                    )
                    if next_was_not_called:
                        if middleware_resp is not None:
                            if self._framework_logger.level <= logging.DEBUG:
                                debug_message = debug_return_listener_middleware_response(
                                    listener_name,
                                    middleware_resp.status,
                                    middleware_resp.body,
                                    starting_time,
                                )
                                self._framework_logger.debug(debug_message)
                            return middleware_resp
                        # The last listener middleware didn't call next() method.
                        # This means the listener is not for this incoming request.
                        continue

                    if middleware_resp is not None:
                        resp = middleware_resp

                    self._framework_logger.debug(debug_running_listener(listener_name))
                    listener_response: Optional[BoltResponse] = await self._async_listener_runner.run(
                        request=req,
                        response=resp,  # type: ignore[arg-type]
                        listener_name=listener_name,
                        listener=listener,
                    )
                    if listener_response is not None:
                        return listener_response

            if resp is None:
                resp = BoltResponse(status=404, body={"error": "unhandled request"})
            if self._raise_error_for_unhandled_request is True:
                try:
                    raise BoltUnhandledRequestError(
                        request=req,
                        current_response=resp,
                    )
                except BoltUnhandledRequestError as e:
                    await self._async_listener_runner.listener_error_handler.handle(
                        error=e,
                        request=req,
                        response=resp,
                    )
                return resp
            return self._handle_unmatched_requests(req, resp)

        except Exception as error:
            resp = BoltResponse(status=500, body="")
            await self._async_middleware_error_handler.handle(
                error=error,
                request=req,
                response=resp,
            )
            return resp

    def _handle_unmatched_requests(self, req: AsyncBoltRequest, resp: BoltResponse) -> BoltResponse:
        self._framework_logger.warning(warning_unhandled_request(req))
        return resp

    # -------------------------
    # middleware

    def use(self, *args) -> Optional[Callable]:
        """Refer to `AsyncApp#middleware()` method's docstring for details."""
        return self.middleware(*args)

    def middleware(self, *args) -> Optional[Callable]:
        """Registers a new middleware to this app.
        This method can be used as either a decorator or a method.

            # Use this method as a decorator
            @app.middleware
            async def middleware_func(logger, body, next):
                logger.info(f"request body: {body}")
                await next()

            # Pass a function to this method
            app.middleware(middleware_func)

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

        Args:
            *args: A function that works as a global middleware.
        """
        if len(args) > 0:
            middleware_or_callable = args[0]
            if isinstance(middleware_or_callable, AsyncMiddleware):
                middleware: AsyncMiddleware = middleware_or_callable
                self._async_middleware_list.append(middleware)
                if isinstance(middleware, AsyncAssistant) and middleware.thread_context_store is not None:
                    self._assistant_thread_context_store = middleware.thread_context_store
            elif callable(middleware_or_callable):
                self._async_middleware_list.append(
                    AsyncCustomMiddleware(
                        app_name=self.name,
                        func=middleware_or_callable,
                        base_logger=self._base_logger,
                    )
                )
                return middleware_or_callable
            else:
                raise BoltError(f"Unexpected type for a middleware ({type(middleware_or_callable)})")
        return None

    def assistant(self, assistant: AsyncAssistant) -> Optional[Callable]:
        return self.middleware(assistant)

    # -------------------------
    # Workflows: Steps from apps

    def step(
        self,
        callback_id: Union[str, Pattern, AsyncWorkflowStep, AsyncWorkflowStepBuilder],
        edit: Optional[Union[Callable[..., Optional[BoltResponse]], AsyncListener, Sequence[Callable]]] = None,
        save: Optional[Union[Callable[..., Optional[BoltResponse]], AsyncListener, Sequence[Callable]]] = None,
        execute: Optional[Union[Callable[..., Optional[BoltResponse]], AsyncListener, Sequence[Callable]]] = None,
    ):
        """
        Deprecated:
            Steps from apps for legacy workflows are now deprecated.
            Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

        Registers a new step from app listener.

        Unlike others, this method doesn't behave as a decorator.
        If you want to register a step from app by a decorator, use `AsyncWorkflowStepBuilder`'s methods.

            # Create a new WorkflowStep instance
            from slack_bolt.workflows.async_step import AsyncWorkflowStep
            ws = AsyncWorkflowStep(
                callback_id="add_task",
                edit=edit,
                save=save,
                execute=execute,
            )
            # Pass Step to set up listeners
            app.step(ws)

        Refer to https://docs.slack.dev/legacy/legacy-steps-from-apps/ for details of steps from apps.

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.
        For further information about AsyncWorkflowStep specific function arguments
        such as `configure`, `update`, `complete`, and `fail`,
        refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

        Args:
            callback_id: The Callback ID for this step from app
            edit: The function for displaying a modal in the Workflow Builder
            save: The function for handling configuration in the Workflow Builder
            execute: The function for handling the step execution
        """
        warnings.warn(
            (
                "Steps from apps for legacy workflows are now deprecated. "
                "Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/"
            ),
            category=DeprecationWarning,
        )
        step = callback_id
        if isinstance(callback_id, (str, Pattern)):
            step = AsyncWorkflowStep(
                callback_id=callback_id,
                edit=edit,  # type: ignore[arg-type]
                save=save,  # type: ignore[arg-type]
                execute=execute,  # type: ignore[arg-type]
                base_logger=self._base_logger,
            )
        elif isinstance(step, AsyncWorkflowStepBuilder):
            step = step.build(base_logger=self._base_logger)
        elif not isinstance(step, AsyncWorkflowStep):
            raise BoltError(f"Invalid step object ({type(step)})")

        self.use(AsyncWorkflowStepMiddleware(step))

    # -------------------------
    # global error handler

    def error(
        self, func: Callable[..., Awaitable[Optional[BoltResponse]]]
    ) -> Callable[..., Awaitable[Optional[BoltResponse]]]:
        """Updates the global error handler. This method can be used as either a decorator or a method.

            # Use this method as a decorator
            @app.error
            async def custom_error_handler(error, body, logger):
                logger.exception(f"Error: {error}")
                logger.info(f"Request body: {body}")

            # Pass a function to this method
            app.error(custom_error_handler)

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

        Args:
            func: The function that is supposed to be executed
                when getting an unhandled error in Bolt app.
        """
        if not is_callable_coroutine(func):
            name = get_name_for_callable(func)
            raise BoltError(error_listener_function_must_be_coro_func(name))
        self._async_listener_runner.listener_error_handler = AsyncCustomListenerErrorHandler(
            logger=self._framework_logger,
            func=func,
        )
        self._async_middleware_error_handler = AsyncCustomMiddlewareErrorHandler(
            logger=self._framework_logger,
            func=func,
        )
        return func

    # -------------------------
    # events

    def event(
        self,
        event: Union[
            str,
            Pattern,
            Dict[str, Optional[Union[str, Sequence[Optional[Union[str, Pattern]]]]]],
        ],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new event listener. This method can be used as either a decorator or a method.

            # Use this method as a decorator
            @app.event("team_join")
            async def ask_for_introduction(event, say):
                welcome_channel_id = "C12345"
                user_id = event["user"]
                text = f"Welcome to the team, <@{user_id}>! :tada: You can introduce yourself in this channel."
                await say(text=text, channel=welcome_channel_id)

            # Pass a function to this method
            app.event("team_join")(ask_for_introduction)

        Refer to https://docs.slack.dev/apis/events-api/ for details of Events API.

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

        Args:
            event: The conditions that match a request payload.
                If you pass a dict for this, you can have type, subtype in the constraint.
            matchers: A list of listener matcher functions.
                Only when all the matchers return True, the listener function can be invoked.
            middleware: A list of lister middleware functions.
                Only when all the middleware call `next()` method, the listener function can be invoked.
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.event(event, True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware, True)

        return __call__

    def message(
        self,
        keyword: Union[str, Pattern] = "",
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new message event listener. This method can be used as either a decorator or a method.
        Check the `App#event` method's docstring for details.

            # Use this method as a decorator
            @app.message(":wave:")
            async def say_hello(message, say):
                user = message['user']
                await say(f"Hi there, <@{user}>!")

            # Pass a function to this method
            app.message(":wave:")(say_hello)

        Refer to https://docs.slack.dev/reference/events/message/ for details of `message` events.

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

        Args:
            keyword: The keyword to match
            matchers: A list of listener matcher functions.
                Only when all the matchers return True, the listener function can be invoked.
            middleware: A list of lister middleware functions.
                Only when all the middleware call `next()` method, the listener function can be invoked.
        """
        matchers = list(matchers) if matchers else []
        middleware = list(middleware) if middleware else []

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            constraints = {
                "type": "message",
                "subtype": (
                    # In most cases, new message events come with no subtype.
                    None,
                    # As of Jan 2021, most bot messages no longer have the subtype bot_message.
                    # By contrast, messages posted using classic app's bot token still have the subtype.
                    "bot_message",
                    # If an end-user posts a message with "Also send to #channel" checked,
                    # the message event comes with this subtype.
                    "thread_broadcast",
                    # If an end-user posts a message with attached files,
                    # the message event comes with this subtype.
                    "file_share",
                ),
            }
            primary_matcher = builtin_matchers.message_event(
                constraints=constraints,
                keyword=keyword,
                asyncio=True,
                base_logger=self._base_logger,
            )
            middleware.insert(0, AsyncMessageListenerMatches(keyword))
            return self._register_listener(list(functions), primary_matcher, matchers, middleware, True)

        return __call__

    def function(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
        auto_acknowledge: bool = True,
        ack_timeout: int = 3,
    ) -> Callable[..., Optional[Callable[..., Awaitable[BoltResponse]]]]:
        """Registers a new Function listener.
        This method can be used as either a decorator or a method.

            # Use this method as a decorator
            @app.function("reverse")
            async def reverse_string(ack: AsyncAck, inputs: dict, complete: AsyncComplete, fail: AsyncFail):
                try:
                    await ack()
                    string_to_reverse = inputs["stringToReverse"]
                    await complete({"reverseString": string_to_reverse[::-1]})
                except Exception as e:
                    await fail(f"Cannot reverse string (error: {e})")
                    raise e

            # Pass a function to this method
            app.function("reverse")(reverse_string)

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

        Args:
            callback_id: The callback id to identify the function
            matchers: A list of listener matcher functions.
                Only when all the matchers return True, the listener function can be invoked.
            middleware: A list of lister middleware functions.
                Only when all the middleware call `next()` method, the listener function can be invoked.
        """
        if auto_acknowledge is True:
            if ack_timeout != 3:
                self._framework_logger.warning(warning_ack_timeout_has_no_effect(callback_id, ack_timeout))

        matchers = list(matchers) if matchers else []
        middleware = list(middleware) if middleware else []

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.function_executed(
                callback_id=callback_id, base_logger=self._base_logger, asyncio=True
            )
            return self._register_listener(functions, primary_matcher, matchers, middleware, auto_acknowledge, ack_timeout)

        return __call__

    # -------------------------
    # slash commands

    def command(
        self,
        command: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new slash command listener.
        This method can be used as either a decorator or a method.

            # Use this method as a decorator
            @app.command("/echo")
            async def repeat_text(ack, say, command):
                # Acknowledge command request
                await ack()
                await say(f"{command['text']}")

            # Pass a function to this method
            app.command("/echo")(repeat_text)

        Refer to https://docs.slack.dev/interactivity/implementing-slash-commands/ for details of Slash Commands.

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

        Args:
            command: The conditions that match a request payload
            matchers: A list of listener matcher functions.
                Only when all the matchers return True, the listener function can be invoked.
            middleware: A list of lister middleware functions.
                Only when all the middleware call `next()` method, the listener function can be invoked.
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.command(command, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # shortcut

    def shortcut(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new shortcut listener.
        This method can be used as either a decorator or a method.

            # Use this method as a decorator
            @app.shortcut("open_modal")
            async def open_modal(ack, body, client):
                # Acknowledge the command request
                await ack()
                # Call views_open with the built-in client
                await client.views_open(
                    # Pass a valid trigger_id within 3 seconds of receiving it
                    trigger_id=body["trigger_id"],
                    # View payload
                    view={ ... }
                )

            # Pass a function to this method
            app.shortcut("open_modal")(open_modal)

        Refer to https://docs.slack.dev/interactivity/implementing-shortcuts/ for details about Shortcuts.

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

        Args:
            constraints: The conditions that match a request payload.
            matchers: A list of listener matcher functions.
                Only when all the matchers return True, the listener function can be invoked.
            middleware: A list of lister middleware functions.
                Only when all the middleware call `next()` method, the listener function can be invoked.
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.shortcut(constraints, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    def global_shortcut(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new global shortcut listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.global_shortcut(callback_id, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    def message_shortcut(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new message shortcut listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.message_shortcut(callback_id, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # action

    def action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new action listener. This method can be used as either a decorator or a method.

            # Use this method as a decorator
            @app.action("approve_button")
            async def update_message(ack):
                await ack()

            # Pass a function to this method
            app.action("approve_button")(update_message)

        * Refer to https://docs.slack.dev/reference/interaction-payloads/block_actions-payload/ for actions in `blocks`.
        * Refer to https://docs.slack.dev/legacy/legacy-messaging/legacy-message-buttons/ for actions in `attachments`.
        * Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for actions in dialogs.

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

        Args:
            constraints: The conditions that match a request payload
            matchers: A list of listener matcher functions.
                Only when all the matchers return True, the listener function can be invoked.
            middleware: A list of lister middleware functions.
                Only when all the middleware call `next()` method, the listener function can be invoked.
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.action(constraints, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    def block_action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new `block_actions` action listener.
        Refer to https://docs.slack.dev/reference/interaction-payloads/block_actions-payload/ for details.
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.block_action(constraints, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    def attachment_action(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new `interactive_message` action listener.
        Refer to https://docs.slack.dev/legacy/legacy-messaging/legacy-message-buttons/ for details."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.attachment_action(callback_id, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    def dialog_submission(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new `dialog_submission` listener.
        Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for details."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.dialog_submission(callback_id, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    def dialog_cancellation(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new `dialog_submission` listener.
        Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for details."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.dialog_cancellation(callback_id, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # view

    def view(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new `view_submission`/`view_closed` event listener.
        This method can be used as either a decorator or a method.

            # Use this method as a decorator
            @app.view("view_1")
            async def handle_submission(ack, body, client, view):
                # Assume there's an input block with `block_c` as the block_id and `dreamy_input`
                hopes_and_dreams = view["state"]["values"]["block_c"]["dreamy_input"]
                user = body["user"]["id"]
                # Validate the inputs
                errors = {}
                if hopes_and_dreams is not None and len(hopes_and_dreams) <= 5:
                    errors["block_c"] = "The value must be longer than 5 characters"
                if len(errors) > 0:
                    await ack(response_action="errors", errors=errors)
                    return
                # Acknowledge the view_submission event and close the modal
                await ack()
                # Do whatever you want with the input data - here we're saving it to a DB

            # Pass a function to this method
            app.view("view_1")(handle_submission)

        Refer to https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload for details of payloads.

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

        Args:
            constraints: The conditions that match a request payload
            matchers: A list of listener matcher functions.
                Only when all the matchers return True, the listener function can be invoked.
            middleware: A list of lister middleware functions.
                Only when all the middleware call `next()` method, the listener function can be invoked.
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.view(constraints, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    def view_submission(
        self,
        constraints: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new `view_submission` listener.
        Refer to https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload/#view_submission for
        details.
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.view_submission(constraints, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    def view_closed(
        self,
        constraints: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new `view_closed` listener.
        Refer to https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload/#view_closed for details."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.view_closed(constraints, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # options

    def options(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new options listener.
        This method can be used as either a decorator or a method.

            # Use this method as a decorator
            @app.options("menu_selection")
            async def show_menu_options(ack):
                options = [
                    {
                        "text": {"type": "plain_text", "text": "Option 1"},
                        "value": "1-1",
                    },
                    {
                        "text": {"type": "plain_text", "text": "Option 2"},
                        "value": "1-2",
                    },
                ]
                await ack(options=options)

            # Pass a function to this method
            app.options("menu_selection")(show_menu_options)

        Refer to the following documents for details:

        * https://docs.slack.dev/reference/block-kit/block-elements/select-menu-element#external_select
        * https://docs.slack.dev/reference/block-kit/block-elements/multi-select-menu-element#external_multi_select

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

        Args:
            matchers: A list of listener matcher functions.
                Only when all the matchers return True, the listener function can be invoked.
            middleware: A list of lister middleware functions.
                Only when all the middleware call `next()` method, the listener function can be invoked.
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.options(constraints, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    def block_suggestion(
        self,
        action_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new `block_suggestion` listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.block_suggestion(action_id, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    def dialog_suggestion(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        """Registers a new `dialog_suggestion` listener.
        Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for details."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.dialog_suggestion(callback_id, asyncio=True, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # built-in listener functions

    def default_tokens_revoked_event_listener(
        self,
    ) -> Callable[..., Awaitable[Optional[BoltResponse]]]:
        if self._async_tokens_revocation_listeners is None:
            raise BoltError(error_installation_store_required_for_builtin_listeners())
        return self._async_tokens_revocation_listeners.handle_tokens_revoked_events

    def default_app_uninstalled_event_listener(
        self,
    ) -> Callable[..., Awaitable[Optional[BoltResponse]]]:
        if self._async_tokens_revocation_listeners is None:
            raise BoltError(error_installation_store_required_for_builtin_listeners())
        return self._async_tokens_revocation_listeners.handle_app_uninstalled_events

    def enable_token_revocation_listeners(self) -> None:
        self.event("tokens_revoked")(self.default_tokens_revoked_event_listener())
        self.event("app_uninstalled")(self.default_app_uninstalled_event_listener())

    # -------------------------

    def _init_context(self, req: AsyncBoltRequest):
        req.context["logger"] = get_bolt_app_logger(app_name=self.name, base_logger=self._base_logger)
        req.context["token"] = self._token
        # Prior to version 1.15, when the token is static, self._client was passed to `req.context`.
        # The intention was to avoid creating a new instance per request
        # in the interest of runtime performance/memory footprint optimization.
        # However, developers may want to replace the token held by req.context.client in some situations.
        # In this case, this behavior can result in thread-unsafe data modification on `self._client`.
        # (`self._client` a.k.a. `app.client` is a singleton object per an App instance)
        # Thus, we've changed the behavior to create a new instance per request regardless of token argument
        # in the App initialization starting v1.15.
        # The overhead brought by this change is slight so that we believe that it is ignorable in any cases.
        client_per_request: AsyncWebClient = AsyncWebClient(
            token=self._token,  # this can be None, and it can be set later on
            base_url=self._async_client.base_url,
            timeout=self._async_client.timeout,
            ssl=self._async_client.ssl,
            proxy=self._async_client.proxy,
            session=self._async_client.session,
            trust_env_in_session=self._async_client.trust_env_in_session,
            headers=self._async_client.headers,
            team_id=req.context.team_id,
            logger=self._async_client.logger,
            retry_handlers=(
                self._async_client.retry_handlers.copy() if self._async_client.retry_handlers is not None else None
            ),
        )
        req.context["client"] = client_per_request

        # Most apps do not need this "listener_runner" instance.
        # It is intended for apps that start lazy listeners from their custom global middleware.
        req.context["listener_runner"] = self.listener_runner

        # For AI Agents & Assistants
        if is_assistant_event(req.body):
            assistant = AsyncAssistantUtilities(
                payload=to_event(req.body),  # type:ignore[arg-type]
                context=req.context,
                thread_context_store=self._assistant_thread_context_store,
            )
            req.context["say"] = assistant.say
            req.context["set_status"] = assistant.set_status
            req.context["set_title"] = assistant.set_title
            req.context["set_suggested_prompts"] = assistant.set_suggested_prompts
            req.context["get_thread_context"] = assistant.get_thread_context
            req.context["save_thread_context"] = assistant.save_thread_context

    @staticmethod
    def _to_listener_functions(
        kwargs: dict,
    ) -> Optional[Sequence[Callable[..., Awaitable[Optional[BoltResponse]]]]]:
        if kwargs:
            functions = [kwargs["ack"]]
            for sub in kwargs["lazy"]:
                functions.append(sub)
            return functions
        return None

    def _register_listener(
        self,
        functions: Sequence[Callable[..., Awaitable[Optional[BoltResponse]]]],
        primary_matcher: AsyncListenerMatcher,
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]],
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]],
        auto_acknowledgement: bool = False,
        ack_timeout: int = 3,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        value_to_return = None
        if not isinstance(functions, list):
            functions = list(functions)
        if len(functions) == 1:
            # In the case where the function is registered using decorator,
            # the registration should return the original function.
            value_to_return = functions[0]

        for func in functions:
            if not is_callable_coroutine(func):
                name = get_name_for_callable(func)
                raise BoltError(error_listener_function_must_be_coro_func(name))

        listener_matchers: List[AsyncListenerMatcher] = [
            AsyncCustomListenerMatcher(app_name=self.name, func=f, base_logger=self._base_logger) for f in (matchers or [])
        ]
        listener_matchers.insert(0, primary_matcher)
        listener_middleware = []
        for m in middleware or []:
            if isinstance(m, AsyncMiddleware):
                listener_middleware.append(m)
            elif callable(m) and is_callable_coroutine(m):
                listener_middleware.append(AsyncCustomMiddleware(app_name=self.name, func=m, base_logger=self._base_logger))
            else:
                raise ValueError(error_unexpected_listener_middleware(type(m)))

        self._async_listeners.append(
            AsyncCustomListener(
                app_name=self.name,
                ack_function=functions.pop(0),
                lazy_functions=functions,  # type:ignore[arg-type]
                matchers=listener_matchers,
                middleware=listener_middleware,
                auto_acknowledgement=auto_acknowledgement,
                ack_timeout=ack_timeout,
                base_logger=self._base_logger,
            )
        )

        return value_to_return
