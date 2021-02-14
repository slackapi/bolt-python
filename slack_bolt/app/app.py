import inspect
import json
import logging
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor
from http.server import SimpleHTTPRequestHandler, HTTPServer
from typing import List, Union, Pattern, Callable, Dict, Optional, Sequence

from slack_sdk.errors import SlackApiError
from slack_sdk.oauth.installation_store import InstallationStore
from slack_sdk.web import WebClient

from slack_bolt.authorization import AuthorizeResult
from slack_bolt.authorization.authorize import (
    Authorize,
    InstallationStoreAuthorize,
    CallableAuthorize,
)
from slack_bolt.error import BoltError
from slack_bolt.lazy_listener.thread_runner import ThreadLazyListenerRunner
from slack_bolt.listener.custom_listener import CustomListener
from slack_bolt.listener.listener import Listener
from slack_bolt.listener.listener_error_handler import (
    DefaultListenerErrorHandler,
    CustomListenerErrorHandler,
)
from slack_bolt.listener.thread_runner import ThreadListenerRunner
from slack_bolt.listener_matcher import CustomListenerMatcher
from slack_bolt.listener_matcher import builtins as builtin_matchers
from slack_bolt.listener_matcher.listener_matcher import ListenerMatcher
from slack_bolt.logger import get_bolt_app_logger, get_bolt_logger
from slack_bolt.logger.messages import (
    warning_client_prioritized_and_token_skipped,
    warning_token_skipped,
    error_auth_test_failure,
    error_token_required,
    warning_unhandled_request,
    debug_checking_listener,
    debug_applying_middleware,
    debug_running_listener,
    error_unexpected_listener_middleware,
    error_client_invalid_type,
    error_authorize_conflicts,
    warning_bot_only_conflicts,
    debug_return_listener_middleware_response,
)
from slack_bolt.middleware import (
    Middleware,
    SslCheck,
    RequestVerification,
    SingleTeamAuthorization,
    MultiTeamsAuthorization,
    IgnoringSelfEvents,
    CustomMiddleware,
)
from slack_bolt.middleware.message_listener_matches import MessageListenerMatches
from slack_bolt.middleware.url_verification import UrlVerification
from slack_bolt.oauth import OAuthFlow
from slack_bolt.oauth.internals import select_consistent_installation_store
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_bolt.util.utils import (
    create_web_client,
    get_boot_message,
    get_name_for_callable,
)
from slack_bolt.workflows.step import WorkflowStep, WorkflowStepMiddleware
from slack_bolt.workflows.step.step import WorkflowStepBuilder


class App:
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
        token_verification_enabled: bool = True,
        client: Optional[WebClient] = None,
        # for multi-workspace apps
        authorize: Optional[Callable[..., AuthorizeResult]] = None,
        installation_store: Optional[InstallationStore] = None,
        # for v1.0.x compatibility
        installation_store_bot_only: Optional[bool] = None,
        # for the OAuth flow
        oauth_settings: Optional[OAuthSettings] = None,
        oauth_flow: Optional[OAuthFlow] = None,
        # No need to set (the value is used only in response to ssl_check requests)
        verification_token: Optional[str] = None,
    ):
        """Bolt App that provides functionalities to register middleware/listeners

        :param name: The application name that will be used in logging.
            If absent, the source file name will be used instead.
        :param process_before_response: True if this app runs on Function as a Service. (Default: False)
        :param signing_secret: The Signing Secret value used for verifying requests from Slack.
        :param token: The bot access token required only for single-workspace app.
        :param token_verification_enabled: Verifies the validity of the given token if True.
        :param client: The singleton slack_sdk.WebClient instance for this app.
        :param authorize: The function to authorize an incoming request from Slack
            by checking if there is a team/user in the installation data.
        :param installation_store: The module offering save/find operations of installation data
        :param installation_store_bot_only: Use InstallationStore#find_bot if True (Default: False)
        :param oauth_settings: The settings related to Slack app installation flow (OAuth flow)
        :param oauth_flow: Manually instantiated slack_bolt.oauth.OAuthFlow.
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
        self._framework_logger = logger or get_bolt_logger(App)

        self._token: Optional[str] = token

        if client is not None:
            if not isinstance(client, WebClient):
                raise BoltError(error_client_invalid_type())
            self._client = client
            self._token = client.token
            if token is not None:
                self._framework_logger.warning(
                    warning_client_prioritized_and_token_skipped()
                )
        else:
            self._client = create_web_client(token)  # NOTE: the token here can be None

        # --------------------------------------
        # Authorize & OAuthFlow initialization
        # --------------------------------------

        self._authorize: Optional[Authorize] = None
        if authorize is not None:
            if oauth_settings is not None or oauth_flow is not None:
                raise BoltError(error_authorize_conflicts())
            self._authorize = CallableAuthorize(
                logger=self._framework_logger, func=authorize
            )

        self._installation_store: Optional[InstallationStore] = installation_store
        if self._installation_store is not None and self._authorize is None:
            self._authorize = InstallationStoreAuthorize(
                installation_store=self._installation_store,
                logger=self._framework_logger,
                bot_only=installation_store_bot_only,
            )

        self._oauth_flow: Optional[OAuthFlow] = None

        if (
            oauth_settings is None
            and os.environ.get("SLACK_CLIENT_ID") is not None
            and os.environ.get("SLACK_CLIENT_SECRET") is not None
        ):
            # initialize with the default settings
            oauth_settings = OAuthSettings()

        if oauth_flow:
            self._oauth_flow = oauth_flow
            installation_store = select_consistent_installation_store(
                client_id=self._oauth_flow.client_id,
                app_store=self._installation_store,
                oauth_flow_store=self._oauth_flow.settings.installation_store,
                logger=self._framework_logger,
            )
            self._installation_store = installation_store
            self._oauth_flow.settings.installation_store = installation_store

            if self._oauth_flow._client is None:
                self._oauth_flow._client = self._client
            if self._authorize is None:
                self._authorize = self._oauth_flow.settings.authorize
        elif oauth_settings is not None:
            installation_store = select_consistent_installation_store(
                client_id=oauth_settings.client_id,
                app_store=self._installation_store,
                oauth_flow_store=oauth_settings.installation_store,
                logger=self._framework_logger,
            )
            self._installation_store = installation_store
            oauth_settings.installation_store = installation_store
            self._oauth_flow = OAuthFlow(
                client=self.client, logger=self.logger, settings=oauth_settings
            )
            if self._authorize is None:
                self._authorize = self._oauth_flow.settings.authorize

        if (
            self._installation_store is not None or self._authorize is not None
        ) and self._token is not None:
            self._token = None
            self._framework_logger.warning(warning_token_skipped())

        # after setting bot_only here, __init__ cannot replace authorize function
        if installation_store_bot_only is not None and self._oauth_flow is not None:
            app_bot_only = installation_store_bot_only or False
            oauth_flow_bot_only = self._oauth_flow.settings.installation_store_bot_only
            if app_bot_only != oauth_flow_bot_only:
                self.logger.warning(warning_bot_only_conflicts())
                self._oauth_flow.settings.installation_store_bot_only = app_bot_only
                self._authorize.bot_only = app_bot_only

        # --------------------------------------
        # Middleware Initialization
        # --------------------------------------

        self._middleware_list: List[Union[Callable, Middleware]] = []
        self._listeners: List[Listener] = []

        listener_executor = ThreadPoolExecutor(max_workers=5)
        self._listener_runner = ThreadListenerRunner(
            logger=self._framework_logger,
            process_before_response=process_before_response,
            listener_error_handler=DefaultListenerErrorHandler(
                logger=self._framework_logger
            ),
            listener_executor=listener_executor,
            lazy_listener_runner=ThreadLazyListenerRunner(
                logger=self._framework_logger,
                executor=listener_executor,
            ),
        )

        self._init_middleware_list_done = False
        self._init_middleware_list(
            token_verification_enabled=token_verification_enabled
        )

    def _init_middleware_list(self, token_verification_enabled: bool):
        if self._init_middleware_list_done:
            return
        self._middleware_list.append(
            SslCheck(verification_token=self._verification_token)
        )
        self._middleware_list.append(RequestVerification(self._signing_secret))

        if self._oauth_flow is None:
            if self._token is not None:
                try:
                    auth_test_result = None
                    if token_verification_enabled:
                        auth_test_result = self._client.auth_test(token=self._token)
                    self._middleware_list.append(
                        SingleTeamAuthorization(auth_test_result=auth_test_result)
                    )
                except SlackApiError as err:
                    raise BoltError(error_auth_test_failure(err.response))
            elif self._authorize is not None:
                self._middleware_list.append(
                    MultiTeamsAuthorization(authorize=self._authorize)
                )
            else:
                raise BoltError(error_token_required())
        else:
            self._middleware_list.append(
                MultiTeamsAuthorization(authorize=self._authorize)
            )
        self._middleware_list.append(IgnoringSelfEvents())
        self._middleware_list.append(UrlVerification())
        self._init_middleware_list_done = True

    # -------------------------
    # accessors

    @property
    def name(self) -> str:
        return self._name

    @property
    def oauth_flow(self) -> Optional[OAuthFlow]:
        return self._oauth_flow

    @property
    def logger(self) -> logging.Logger:
        return self._framework_logger

    @property
    def client(self) -> WebClient:
        return self._client

    @property
    def installation_store(self) -> Optional[InstallationStore]:
        return self._installation_store

    @property
    def listener_runner(self) -> ThreadListenerRunner:
        return self._listener_runner

    # -------------------------
    # standalone server

    def start(self, port: int = 3000, path: str = "/slack/events") -> None:
        """Start a web server for local development.
        This method internally starts a Web server process built with the http.server module.'
        For production, consider using a production-ready WSGI server such as Gunicorn.

        :param port: The port to listen on (Default: 3000)
        :param path: The path to handle request from Slack (Default: /slack/events)
        :return: None
        """
        self._development_server = SlackAppDevelopmentServer(
            port=port,
            path=path,
            app=self,
            oauth_flow=self.oauth_flow,
        )
        self._development_server.start()

    # -------------------------
    # main dispatcher

    def dispatch(self, req: BoltRequest) -> BoltResponse:
        """Applies all middleware and dispatches an incoming request from Slack to the right code path.

        :param req: An incoming request from Slack.
        :return: The response generated by this Bolt app.
        """
        starting_time = time.time()
        self._init_context(req)

        resp: BoltResponse = BoltResponse(status=200, body="")
        middleware_state = {"next_called": False}

        def middleware_next():
            middleware_state["next_called"] = True

        for middleware in self._middleware_list:
            middleware_state["next_called"] = False
            if self._framework_logger.level <= logging.DEBUG:
                self._framework_logger.debug(debug_applying_middleware(middleware.name))
            resp = middleware.process(req=req, resp=resp, next=middleware_next)
            if not middleware_state["next_called"]:
                if resp is None:
                    return BoltResponse(
                        status=404, body={"error": "no next() calls in middleware"}
                    )
                return resp

        for listener in self._listeners:
            listener_name = get_name_for_callable(listener.ack_function)
            self._framework_logger.debug(debug_checking_listener(listener_name))
            if listener.matches(req=req, resp=resp):
                # run all the middleware attached to this listener first
                middleware_resp, next_was_not_called = listener.run_middleware(
                    req=req, resp=resp
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
                listener_response: Optional[BoltResponse] = self._listener_runner.run(
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
            if isinstance(middleware_or_callable, Middleware):
                self._middleware_list.append(middleware_or_callable)
            elif isinstance(middleware_or_callable, Callable):
                self._middleware_list.append(
                    CustomMiddleware(app_name=self.name, func=middleware_or_callable)
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
        callback_id: Union[str, Pattern, WorkflowStep, WorkflowStepBuilder],
        edit: Optional[
            Union[Callable[..., Optional[BoltResponse]], Listener, Sequence[Callable]]
        ] = None,
        save: Optional[
            Union[Callable[..., Optional[BoltResponse]], Listener, Sequence[Callable]]
        ] = None,
        execute: Optional[
            Union[Callable[..., Optional[BoltResponse]], Listener, Sequence[Callable]]
        ] = None,
    ):
        """Registers a new Workflow Step listener
        Unlike others, this method doesn't behave as a decorator. If you want to register a workflow step
        by a decorator, use WorkflowStepBuilder's methods.
        """
        step = callback_id
        if isinstance(callback_id, (str, Pattern)):
            step = WorkflowStep(
                callback_id=callback_id,
                edit=edit,
                save=save,
                execute=execute,
            )
        elif isinstance(step, WorkflowStepBuilder):
            step = step.build()
        elif not isinstance(step, WorkflowStep):
            raise BoltError(f"Invalid step object ({type(step)})")

        self.use(WorkflowStepMiddleware(step, self.listener_runner))

    # -------------------------
    # global error handler

    def error(
        self, func: Callable[..., None]
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Updates the global error handler.

        :param func: The function that is supposed to be executed
            when getting an unhandled error in Bolt app.
        :return: None
        """
        self._listener_runner.listener_error_handler = CustomListenerErrorHandler(
            logger=self._framework_logger,
            func=func,
        )
        return func

    # -------------------------
    # events

    def event(
        self,
        event: Union[
            str, Pattern, Dict[str, Union[str, Sequence[Optional[Union[str, Pattern]]]]]
        ],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new event listener.

        :param event: The conditions to match against a request payload
        :param matchers: A list of listener matcher functions.
        :param middleware: A list of lister middleware functions.
        :return: None
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.event(event)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware, True
            )

        return __call__

    def message(
        self,
        keyword: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new message event listener.
        Check the #event method's docstring for details.
        """
        matchers = list(matchers) if matchers else []
        middleware = list(middleware) if middleware else []

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            # As of Jan 2021, most bot messages no longer have the subtype bot_message.
            # By contrast, messages posted using classic app's bot token still have the subtype.
            constraints = {"type": "message", "subtype": (None, "bot_message")}
            primary_matcher = builtin_matchers.event(constraints=constraints)
            middleware.insert(0, MessageListenerMatches(keyword))
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware, True
            )

        return __call__

    # -------------------------
    # slash commands

    def command(
        self,
        command: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new slash command listener.

        :param command: The conditions to match against a request payload
        :param matchers: A list of listener matcher functions.
        :param middleware: A list of lister middleware functions.
        :return: None
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.command(command)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    # -------------------------
    # shortcut

    def shortcut(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new shortcut listener.

        :param constraints: The conditions to match against a request payload
        :param matchers: A list of listener matcher functions.
        :param middleware: A list of lister middleware functions.
        :return: None
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.shortcut(constraints)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def global_shortcut(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new global shortcut listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.global_shortcut(callback_id)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def message_shortcut(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new message shortcut listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.message_shortcut(callback_id)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    # -------------------------
    # action

    def action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new action listener.

        :param constraints: The conditions to match against a request payload
        :param matchers: A list of listener matcher functions.
        :param middleware: A list of lister middleware functions.
        :return: None
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.action(constraints)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def block_action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new block_actions listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.block_action(constraints)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def attachment_action(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new interactive_message listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.attachment_action(callback_id)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def dialog_submission(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new dialog_submission listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.dialog_submission(callback_id)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def dialog_cancellation(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new dialog_cancellation listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.dialog_cancellation(callback_id)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    # -------------------------
    # view

    def view(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new view submission/closed event listener.

        :param constraints: The conditions to match against a request payload
        :param matchers: A list of listener matcher functions.
        :param middleware: A list of lister middleware functions.
        :return: None
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.view(constraints)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def view_submission(
        self,
        constraints: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new view_submission listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.view_submission(constraints)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def view_closed(
        self,
        constraints: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new view_closed listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.view_closed(constraints)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    # -------------------------
    # options

    def options(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new options listener.

        :param constraints: The conditions to match against a request payload
        :param matchers: A list of listener matcher functions.
        :param middleware: A list of lister middleware functions.
        :return: None
        """

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.options(constraints)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def block_suggestion(
        self,
        action_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new block_suggestion listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.block_suggestion(action_id)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    def dialog_suggestion(
        self,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        """Registers a new dialog_submission listener."""

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.dialog_suggestion(callback_id)
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware
            )

        return __call__

    # -------------------------

    def _init_context(self, req: BoltRequest):
        req.context["logger"] = get_bolt_app_logger(self.name)
        req.context["token"] = self._token
        if self._token is not None:
            # This WebClient instance can be safely singleton
            req.context["client"] = self._client
        else:
            # Set a new dedicated instance for this request
            client_per_request: WebClient = WebClient(
                token=None,  # the token will be set later
                base_url=self._client.base_url,
                timeout=self._client.timeout,
                ssl=self._client.ssl,
                proxy=self._client.proxy,
                headers=self._client.headers,
                team_id=req.context.team_id,
            )
            req.context["client"] = client_per_request

    @staticmethod
    def _to_listener_functions(
        kwargs: dict,
    ) -> Optional[Sequence[Callable[..., Optional[BoltResponse]]]]:
        if kwargs:
            functions = [kwargs["ack"]]
            for sub in kwargs["lazy"]:
                functions.append(sub)
            return functions
        return None

    def _register_listener(
        self,
        functions: Sequence[Callable[..., Optional[BoltResponse]]],
        primary_matcher: ListenerMatcher,
        matchers: Optional[Sequence[Callable[..., bool]]],
        middleware: Optional[Sequence[Union[Callable, Middleware]]],
        auto_acknowledgement: bool = False,
    ) -> Optional[Callable[..., Optional[BoltResponse]]]:
        value_to_return = None
        if not isinstance(functions, list):
            functions = list(functions)
        if len(functions) == 1:
            # In the case where the function is registered using decorator,
            # the registration should return the original function.
            value_to_return = functions[0]

        listener_matchers = [
            CustomListenerMatcher(app_name=self.name, func=f) for f in (matchers or [])
        ]
        listener_matchers.insert(0, primary_matcher)
        listener_middleware = []
        for m in middleware or []:
            if isinstance(m, Middleware):
                listener_middleware.append(m)
            elif isinstance(m, Callable):
                listener_middleware.append(CustomMiddleware(app_name=self.name, func=m))
            else:
                raise ValueError(error_unexpected_listener_middleware(type(m)))

        self._listeners.append(
            CustomListener(
                app_name=self.name,
                ack_function=functions.pop(0),
                lazy_functions=functions,
                matchers=listener_matchers,
                middleware=listener_middleware,
                auto_acknowledgement=auto_acknowledgement,
            )
        )
        return value_to_return


# -------------------------


class SlackAppDevelopmentServer:
    def __init__(
        self,
        port: int,
        path: str,
        app: App,
        oauth_flow: Optional[OAuthFlow] = None,
    ):
        """Slack App Development Server

        This is a thin wrapper of http.server.HTTPServer and is good enough
        for your local development or prototyping.

        However, as mentioned in Python official documents, using http.server module in production
        is not recommended. Please consider using an adapter (refer to slack_bolt.adapter.*)
        along with a production-grade server when running the app for end users.
        https://docs.python.org/3/library/http.server.html#http.server.HTTPServer
        """
        self._port: int = port
        self._bolt_endpoint_path: str = path
        self._bolt_app: App = app
        self._bolt_oauth_flow: Optional[OAuthFlow] = oauth_flow

        _port: int = self._port
        _bolt_endpoint_path: str = self._bolt_endpoint_path
        _bolt_app: App = self._bolt_app
        _bolt_oauth_flow: Optional[OAuthFlow] = self._bolt_oauth_flow

        class SlackAppHandler(SimpleHTTPRequestHandler):
            def do_GET(self):
                if _bolt_oauth_flow:
                    request_path, _, query = self.path.partition("?")
                    if request_path == _bolt_oauth_flow.install_path:
                        bolt_req = BoltRequest(
                            body="", query=query, headers=self.headers
                        )
                        bolt_resp = _bolt_oauth_flow.handle_installation(bolt_req)
                        self._send_bolt_response(bolt_resp)
                    elif request_path == _bolt_oauth_flow.redirect_uri_path:
                        bolt_req = BoltRequest(
                            body="", query=query, headers=self.headers
                        )
                        bolt_resp = _bolt_oauth_flow.handle_callback(bolt_req)
                        self._send_bolt_response(bolt_resp)
                    else:
                        self._send_response(404, headers={})
                else:
                    self._send_response(404, headers={})

            def do_POST(self):
                request_path, _, query = self.path.partition("?")
                if _bolt_endpoint_path != request_path:
                    self._send_response(404, headers={})
                    return

                len_header = self.headers.get("Content-Length") or 0
                request_body = self.rfile.read(int(len_header)).decode("utf-8")
                bolt_req = BoltRequest(
                    body=request_body, query=query, headers=self.headers
                )
                bolt_resp: BoltResponse = _bolt_app.dispatch(bolt_req)
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
                headers: Dict[str, Sequence[str]],
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

        self._server = HTTPServer(("0.0.0.0", self._port), SlackAppHandler)

    def start(self) -> None:
        """Starts a new web server process.

        :return: None
        """
        if self._bolt_app.logger.level > logging.INFO:
            print(get_boot_message(development_server=True))
        else:
            self._bolt_app.logger.info(get_boot_message(development_server=True))

        try:
            self._server.serve_forever(0.05)
        finally:
            self._server.server_close()
