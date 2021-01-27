import inspect
import logging
import os
import time
from typing import Optional, List, Union, Callable, Pattern, Dict, Awaitable, Sequence

from aiohttp import web

from slack_bolt.app.async_server import AsyncSlackAppServer
from slack_bolt.listener.asyncio_runner import AsyncioListenerRunner
from slack_bolt.middleware.message_listener_matches.async_message_listener_matches import (
    AsyncMessageListenerMatches,
)
from slack_bolt.oauth.async_internals import select_consistent_installation_store
from slack_bolt.util.utils import get_name_for_callable
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
from slack_bolt.error import BoltError
from slack_bolt.logger.messages import (
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
        # Basic Information > Credentials > Signing Secret
        signing_secret: Optional[str] = None,
        # for single-workspace apps
        token: Optional[str] = None,
        client: Optional[AsyncWebClient] = None,
        # for multi-workspace apps
        installation_store: Optional[AsyncInstallationStore] = None,
        installation_store_bot_only: Optional[bool] = None,
        authorize: Optional[Callable[..., Awaitable[AuthorizeResult]]] = None,
        # for the OAuth flow
        oauth_settings: Optional[AsyncOAuthSettings] = None,
        oauth_flow: Optional[AsyncOAuthFlow] = None,
        # No need to set (the value is used only in response to ssl_check requests)
        verification_token: Optional[str] = None,
    ):
        """Bolt App that provides functionalities to register middleware/listeners

        :param name: The application name that will be used in logging.
            If absent, the source file name will be used instead.
        :param process_before_response: True if this app runs on Function as a Service. (Default: False)
        :param signing_secret: The Signing Secret value used for verifying requests from Slack.
        :param token: The bot access token required only for single-workspace app.
        :param client: The singleton slack_sdk.web.async_client.AsyncWebClient instance for this app.
        :param installation_store: The module offering save/find operations of installation data
        :param installation_store_bot_only: Use InstallationStore#find_bot if True (Default: False)
        :param authorize: The function to authorize an incoming request from Slack
            by checking if there is a team/user in the installation data.
        :param oauth_settings: The settings related to Slack app installation flow (OAuth flow)
        :param oauth_flow: Manually instantiated slack_bolt.oauth.async_oauth_flow.AsyncOAuthFlow.
            This is always prioritized over oauth_settings.
        :param verification_token: Deprecated verification mechanism.
            This can used only for ssl_check requests.
        """
        signing_secret = signing_secret or os.environ.get("SLACK_SIGNING_SECRET")
        token = token or os.environ.get("SLACK_BOT_TOKEN")

        self._name: str = name or inspect.stack()[1].filename.split(os.path.sep)[-1]
        self._signing_secret: str = signing_secret
        self._verification_token: Optional[str] = verification_token or os.environ.get(
            "SLACK_VERIFICATION_TOKEN", None
        )
        self._framework_logger = logger or get_bolt_logger(AsyncApp)

        self._token: Optional[str] = token

        if client is not None:
            if not isinstance(client, AsyncWebClient):
                raise BoltError(error_client_invalid_type_async())
            self._async_client = client
            self._token = client.token
            if token is not None:
                self._framework_logger.warning(
                    warning_client_prioritized_and_token_skipped()
                )
        else:
            # NOTE: the token here can be None
            self._async_client = create_async_web_client(token)

        # --------------------------------------
        # Authorize & OAuthFlow initialization
        # --------------------------------------

        self._async_authorize: Optional[AsyncAuthorize] = None
        if authorize is not None:
            if oauth_settings is not None or oauth_flow is not None:
                raise BoltError(error_authorize_conflicts())

            self._async_authorize = AsyncCallableAuthorize(
                logger=self._framework_logger, func=authorize
            )

        self._async_installation_store: Optional[
            AsyncInstallationStore
        ] = installation_store
        if self._async_installation_store is not None and self._async_authorize is None:
            self._async_authorize = AsyncInstallationStoreAuthorize(
                installation_store=self._async_installation_store,
                logger=self._framework_logger,
                bot_only=installation_store_bot_only,
            )

        self._async_oauth_flow: Optional[AsyncOAuthFlow] = None

        if (
            oauth_settings is None
            and os.environ.get("SLACK_CLIENT_ID") is not None
            and os.environ.get("SLACK_CLIENT_SECRET") is not None
        ):
            # initialize with the default settings
            oauth_settings = AsyncOAuthSettings()

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
            oauth_settings.installation_store = installation_store

            self._async_oauth_flow = AsyncOAuthFlow(
                client=self._async_client, logger=self.logger, settings=oauth_settings
            )
            if self._async_authorize is None:
                self._async_authorize = self._async_oauth_flow.settings.authorize

        if (
            self._async_installation_store is not None
            or self._async_authorize is not None
        ) and self._token is not None:
            self._token = None
            self._framework_logger.warning(warning_token_skipped())

        # after setting bot_only here, __init__ cannot replace authorize function
        if (
            installation_store_bot_only is not None
            and self._async_oauth_flow is not None
        ):
            app_bot_only = installation_store_bot_only or False
            oauth_flow_bot_only = (
                self._async_oauth_flow.settings.installation_store_bot_only
            )
            if app_bot_only != oauth_flow_bot_only:
                self.logger.warning(warning_bot_only_conflicts())
                self._async_oauth_flow.settings.installation_store_bot_only = (
                    app_bot_only
                )
                self._async_authorize.bot_only = app_bot_only

        # --------------------------------------
        # Middleware Initialization
        # --------------------------------------

        self._async_middleware_list: List[Union[Callable, AsyncMiddleware]] = []
        self._async_listeners: List[AsyncListener] = []

        self._async_listener_runner = AsyncioListenerRunner(
            logger=self._framework_logger,
            process_before_response=process_before_response,
            listener_error_handler=AsyncDefaultListenerErrorHandler(
                logger=self._framework_logger
            ),
            lazy_listener_runner=AsyncioLazyListenerRunner(
                logger=self._framework_logger,
            ),
        )

        self._init_middleware_list_done = False
        self._init_async_middleware_list()

        self._server: Optional[AsyncSlackAppServer] = None

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
            elif self._async_authorize is not None:
                self._async_middleware_list.append(
                    AsyncMultiTeamsAuthorization(authorize=self._async_authorize)
                )
            else:
                raise BoltError(error_token_required())
        else:
            self._async_middleware_list.append(
                AsyncMultiTeamsAuthorization(authorize=self._async_authorize)
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
    def listener_runner(self) -> AsyncioListenerRunner:
        return self._async_listener_runner

    # -------------------------
    # standalone server

    from .async_server import AsyncSlackAppServer

    def server(
        self, port: int = 3000, path: str = "/slack/events"
    ) -> AsyncSlackAppServer:
        """Configure a web server using AIOHTTP.

        :param port: The port to listen on (Default: 3000)
        :param path: The path to handle request from Slack (Default: /slack/events)
        :return: None
        """
        if (
            self._server is None
            or self._server.port != port
            or self._server.path != path
        ):
            self._server = AsyncSlackAppServer(
                port=port,
                path=path,
                app=self,
            )
        return self._server

    def web_app(self, path: str = "/slack/events") -> web.Application:
        return self.server(path=path).web_app

    def start(self, port: int = 3000, path: str = "/slack/events") -> None:
        """Start a web server using AIOHTTP.

        :param port: The port to listen on (Default: 3000)
        :param path: The path to handle request from Slack (Default: /slack/events)
        :return: None
        """
        self.server(port=port, path=path).start()

    # -------------------------
    # main dispatcher

    async def async_dispatch(self, req: AsyncBoltRequest) -> BoltResponse:
        """Applies all middleware and dispatches an incoming request from Slack to the right code path.

        :param req: An incoming request from Slack.
        :return: The response generated by this Bolt app.
        """
        starting_time = time.time()
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
                if resp is None:
                    return BoltResponse(
                        status=404, body={"error": "no next() calls in middleware"}
                    )
                return resp

        for listener in self._async_listeners:
            listener_name = get_name_for_callable(listener.ack_function)
            self._framework_logger.debug(debug_checking_listener(listener_name))
            if await listener.async_matches(req=req, resp=resp):
                # run all the middleware attached to this listener first
                (
                    middleware_resp,
                    next_was_not_called,
                ) = await listener.run_async_middleware(req=req, resp=resp)
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
                listener_response: Optional[
                    BoltResponse
                ] = await self._async_listener_runner.run(
                    request=req,
                    response=resp,
                    listener_name=listener_name,
                    listener=listener,
                )
                if listener_response is not None:
                    return listener_response

        self._framework_logger.warning(warning_unhandled_request(req))
        return BoltResponse(status=404, body={"error": "unhandled request"})

    # -------------------------
    # middleware

    def use(self, *args) -> Optional[Callable]:
        """Refer to middleware method's docstring for details."""
        return self.middleware(*args)

    def middleware(self, *args) -> Optional[Callable]:
        """Registers a new middleware to this Bolt app.

        :param args: a list of middleware. Passing a single middleware is supported.
        :return: None
        """
        if len(args) > 0:
            middleware_or_callable = args[0]
            if isinstance(middleware_or_callable, AsyncMiddleware):
                self._async_middleware_list.append(middleware_or_callable)
            elif isinstance(middleware_or_callable, Callable):
                self._async_middleware_list.append(
                    AsyncCustomMiddleware(
                        app_name=self.name, func=middleware_or_callable
                    )
                )
                return middleware_or_callable
            else:
                raise BoltError(
                    f"Unexpected type for a middleware ({type(middleware_or_callable)})"
                )
        return None

    # -------------------------
    # Workflows: Steps from Apps

    def step(
        self,
        callback_id: Union[str, Pattern, AsyncWorkflowStep, AsyncWorkflowStepBuilder],
        edit: Optional[
            Union[
                Callable[..., Optional[BoltResponse]], AsyncListener, Sequence[Callable]
            ]
        ] = None,
        save: Optional[
            Union[
                Callable[..., Optional[BoltResponse]], AsyncListener, Sequence[Callable]
            ]
        ] = None,
        execute: Optional[
            Union[
                Callable[..., Optional[BoltResponse]], AsyncListener, Sequence[Callable]
            ]
        ] = None,
    ):
        """Registers a new Workflow Step listener
        Unlike others, this method doesn't behave as a decorator. If you want to register a workflow step
        by a decorator, use AsyncWorkflowStepBuilder's methods.
        """
        step = callback_id
        if isinstance(callback_id, (str, Pattern)):
            step = AsyncWorkflowStep(
                callback_id=callback_id,
                edit=edit,
                save=save,
                execute=execute,
            )
        elif isinstance(step, AsyncWorkflowStepBuilder):
            step = step.build()
        elif not isinstance(step, AsyncWorkflowStep):
            raise BoltError(f"Invalid step object ({type(step)})")

        self.use(AsyncWorkflowStepMiddleware(step, self._async_listener_runner))

    # -------------------------
    # global error handler

    def error(
        self, func: Callable[..., Awaitable[None]]
    ) -> Callable[..., Awaitable[None]]:
        """Updates the global error handler.

        :param func: The function that is supposed to be executed
            when getting an unhandled error in Bolt app.
        :return: None
        """
        self._async_listener_runner.listener_error_handler = (
            AsyncCustomListenerErrorHandler(
                logger=self._framework_logger,
                func=func,
            )
        )
        return func

    # -------------------------
    # events

    def event(
        self,
        event: Union[
            str, Pattern, Dict[str, Union[str, Sequence[Optional[Union[str, Pattern]]]]]
        ],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new event listener.

        :param event: The conditions to match against a request payload
        :param matchers: A list of listener matcher functions.
        :param middleware: A list of lister middleware functions.
        :return: None
        """

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Register a new message event listener."""
        matchers = list(matchers) if matchers else []
        middleware = list(middleware) if middleware else []

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            # As of Jan 2021, most bot messages no longer have the subtype bot_message.
            # By contrast, messages posted using class app's bot token still have the subtype.
            constraints = {"type": "message", "subtype": (None, "bot_message")}
            primary_matcher = builtin_matchers.event(
                constraints=constraints, asyncio=True
            )
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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new slash command listener.

        :param command: The conditions to match against a request payload
        :param matchers: A list of listener matcher functions.
        :param middleware: A list of lister middleware functions.
        :return: None
        """

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new shortcut listener.

        :param constraints: The conditions to match against a request payload
        :param matchers: A list of listener matcher functions.
        :param middleware: A list of lister middleware functions.
        :return: None
        """

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new global shortcut listener."""

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new message shortcut listener."""

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new action listener.

        :param constraints: The conditions to match against a request payload
        :param matchers: A list of listener matcher functions.
        :param middleware: A list of lister middleware functions.
        :return: None
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.action(constraints, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def block_action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new block_actions listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.block_action(constraints, True)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def attachment_action(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new interactive_message listener."""

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new dialog_submission listener."""

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new dialog_cancellation listener."""

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new view submission/closed listener.

        :param constraints: The conditions to match against a request payload
        :param matchers: A list of listener matcher functions.
        :param middleware: A list of lister middleware functions.
        :return: None
        """

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new view_submission listener."""

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new view_closed listener."""

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new options listener.

        :param constraints: The conditions to match against a request payload
        :param matchers: A list of listener matcher functions.
        :param middleware: A list of lister middleware functions.
        :return: None
        """

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new block_suggestion listener."""

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
        matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
        middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        """Registers a new dialog_submission listener."""

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
        if self._token is not None:
            # This AsyncWebClient instance can be safely singleton
            req.context["client"] = self._async_client
        else:
            # Set a new dedicated instance for this request
            client_per_request: AsyncWebClient = AsyncWebClient(
                token=None,  # the token will be set later
                base_url=self._async_client.base_url,
                timeout=self._async_client.timeout,
                ssl=self._async_client.ssl,
                proxy=self._async_client.proxy,
                session=self._async_client.session,
                trust_env_in_session=self._async_client.trust_env_in_session,
                headers=self._async_client.headers,
                team_id=req.context.team_id,
            )
            req.context["client"] = client_per_request

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
    ) -> Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]:
        value_to_return = None
        if not isinstance(functions, list):
            functions = list(functions)
        if len(functions) == 1:
            # In the case where the function is registered using decorator,
            # the registration should return the original function.
            value_to_return = functions[0]

        for func in functions:
            if not inspect.iscoroutinefunction(func):
                name = get_name_for_callable(func)
                raise BoltError(error_listener_function_must_be_coro_func(name))

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
                raise ValueError(error_unexpected_listener_middleware(type(m)))

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

        return value_to_return
