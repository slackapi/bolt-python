import inspect
import json
import logging
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor
from http.server import SimpleHTTPRequestHandler, HTTPServer
from typing import List, Union, Pattern, Callable, Dict, Optional

from slack_sdk.errors import SlackApiError
from slack_sdk.oauth.installation_store import InstallationStore
from slack_sdk.web import WebClient

from slack_bolt.error import BoltError
from slack_bolt.lazy_listener.runner import LazyListenerRunner
from slack_bolt.lazy_listener.thread_runner import ThreadLazyListenerRunner
from slack_bolt.listener.custom_listener import CustomListener
from slack_bolt.listener.listener import Listener
from slack_bolt.listener.listener_error_handler import (
    ListenerErrorHandler,
    DefaultListenerErrorHandler,
    CustomListenerErrorHandler,
)
from slack_bolt.listener_matcher import CustomListenerMatcher
from slack_bolt.listener_matcher import builtins as builtin_matchers
from slack_bolt.listener_matcher.listener_matcher import ListenerMatcher
from slack_bolt.logger import get_bolt_app_logger, get_bolt_logger
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
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_bolt.util.utils import create_web_client, create_copy


class App:
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
        client: Optional[WebClient] = None,
        # for multi-workspace apps
        installation_store: Optional[InstallationStore] = None,
        # for the OAuth flow
        oauth_settings: Optional[OAuthSettings] = None,
        oauth_flow: Optional[OAuthFlow] = None,
        authorization_test_enabled: bool = True,
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

        self._verification_token: Optional[str] = verification_token or os.environ.get(
            "SLACK_VERIFICATION_TOKEN", None
        )
        self._framework_logger = get_bolt_logger(App)

        self._token: Optional[str] = token

        if client is not None:
            if not isinstance(client, WebClient):
                raise BoltError("client must be a WebClient")
            self._client = client
            self._token = client.token
            if token is not None:
                self._framework_logger.warning(
                    "As you gave client as well, the bot token will be unused."
                )
        else:
            self._client = create_web_client(token)  # NOTE: the token here can be None

        self._installation_store: Optional[InstallationStore] = installation_store

        self._oauth_flow: Optional[OAuthFlow] = None
        self._authorization_test_enabled = authorization_test_enabled
        if oauth_flow:
            self._oauth_flow = oauth_flow
            if self._installation_store is None:
                self._installation_store = self._oauth_flow.settings.installation_store
            if self._oauth_flow._client is None:
                self._oauth_flow._client = self._client
        elif oauth_settings is not None:
            if self._installation_store:
                # Consistently use a single installation_store
                oauth_settings.installation_store = self._installation_store

            self._oauth_flow = OAuthFlow(
                client=self.client, logger=self.logger, settings=oauth_settings
            )

        if self._installation_store is not None and self._token is not None:
            self._token = None
            self._framework_logger.warning(
                "As you gave installation_store as well, the bot token will be unused."
            )

        self._middleware_list: List[Union[Callable, Middleware]] = []
        self._listeners: List[Listener] = []
        self._listener_executor = ThreadPoolExecutor(max_workers=5)  # TODO: shutdown
        self._listener_error_handler = DefaultListenerErrorHandler(
            logger=self._framework_logger
        )
        self._process_before_response = process_before_response

        self.lazy_listener_runner: LazyListenerRunner = ThreadLazyListenerRunner(
            logger=self._framework_logger, executor=self._listener_executor,
        )

        self._init_middleware_list_done = False
        self._init_middleware_list()

    def _init_middleware_list(self):
        if self._init_middleware_list_done:
            return
        self._middleware_list.append(
            SslCheck(verification_token=self._verification_token)
        )
        self._middleware_list.append(RequestVerification(self._signing_secret))

        if self._oauth_flow is None:
            if self._token:
                if self._authorization_test_enabled:
                    self._middleware_list.append(SingleTeamAuthorization())
                else:
                    try:
                        auth_test_result = self._client.auth_test(token=self._token)
                        self._middleware_list.append(
                            SingleTeamAuthorization(
                                auth_test_result=auth_test_result,
                                verification_enabled=self._authorization_test_enabled,
                            )
                        )
                    except SlackApiError as err:
                        raise BoltError(
                            f"token is invalid (auth.test result: {err.response})"
                        )
            else:
                raise BoltError(
                    "Either an env variable SLACK_BOT_TOKEN or token argument in constructor is required."
                )
        else:
            self._middleware_list.append(
                MultiTeamsAuthorization(
                    installation_store=self._installation_store,
                    verification_enabled=self._authorization_test_enabled,
                )
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
    def listener_error_handler(self) -> ListenerErrorHandler:
        return self._listener_error_handler

    # -------------------------
    # standalone server

    def start(self, port: int = 3000, path: str = "/slack/events") -> None:
        self._development_server = SlackAppDevelopmentServer(
            port=port, path=path, app=self, oauth_flow=self.oauth_flow,
        )
        self._development_server.start()

    # -------------------------
    # main dispatcher

    def dispatch(self, req: BoltRequest) -> BoltResponse:
        self._init_context(req)

        resp: BoltResponse = BoltResponse(status=200, body="")
        middleware_state = {"next_called": False}

        def middleware_next():
            middleware_state["next_called"] = True

        for middleware in self._middleware_list:
            middleware_state["next_called"] = False
            if self._framework_logger.level <= logging.DEBUG:
                self._framework_logger.debug(f"Applying {middleware.name}")
            resp = middleware.process(req=req, resp=resp, next=middleware_next)
            if not middleware_state["next_called"]:
                if resp is None:
                    return BoltResponse(
                        status=404, body={"error": "no next() calls in middleware"}
                    )
                return resp

        for listener in self._listeners:
            listener_name = listener.ack_function.__name__
            self._framework_logger.debug(f"Checking listener: {listener_name} ...")
            if listener.matches(req=req, resp=resp):
                # run all the middleware attached to this listener first
                resp, next_was_not_called = listener.run_middleware(req=req, resp=resp)
                if next_was_not_called:
                    # The last listener middleware didn't call next() method.
                    # This means the listener is not for this incoming request.
                    continue

                self._framework_logger.debug(f"Running listener: {listener_name} ...")
                listener_response: Optional[BoltResponse] = self.run_listener(
                    request=req,
                    response=resp,
                    listener_name=listener_name,
                    listener=listener,
                )
                if listener_response is not None:
                    return listener_response

        self._framework_logger.warning(f"Unhandled request ({req.body})")
        return BoltResponse(status=404, body={"error": "unhandled request"})

    def run_listener(
        self,
        request: BoltRequest,
        response: BoltResponse,
        listener_name: str,
        listener: Listener,
    ) -> Optional[BoltResponse]:
        ack = request.context.ack
        starting_time = time.time()
        if self._process_before_response:
            if not request.lazy_only:
                try:
                    returned_value = listener.run_ack_function(
                        request=request, response=response
                    )
                    if isinstance(returned_value, BoltResponse):
                        response = returned_value
                    if ack.response is None and listener.auto_acknowledgement:
                        ack()  # automatic ack() call if the call is not yet done
                except Exception as e:
                    # The default response status code is 500 in this case.
                    # You can customize this by passing your own error handler.
                    if response is None:
                        response = BoltResponse(status=500)
                    response.status = 500
                    self._listener_error_handler.handle(
                        error=e, request=request, response=response,
                    )
                    ack.response = response

            for lazy_func in listener.lazy_functions:
                if request.lazy_function_name:
                    func_name = lazy_func.__name__
                    if func_name == request.lazy_function_name:
                        self.lazy_listener_runner.run(
                            function=lazy_func, request=request
                        )
                        # This HTTP response won't be sent to Slack API servers.
                        return BoltResponse(status=200)
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
            if listener.auto_acknowledgement:
                # acknowledge immediately in case of Events API
                ack()

            if not request.lazy_only:
                # start the listener function asynchronously
                def run_ack_function_asynchronously():
                    nonlocal ack, request, response
                    try:
                        listener.run_ack_function(request=request, response=response)
                    except Exception as e:
                        # The default response status code is 500 in this case.
                        # You can customize this by passing your own error handler.
                        if listener.auto_acknowledgement:
                            self._listener_error_handler.handle(
                                error=e, request=request, response=response,
                            )
                        else:
                            if response is None:
                                response = BoltResponse(status=500)
                            response.status = 500
                            if ack.response is not None:  # already acknowledged
                                response = None
                            self._listener_error_handler.handle(
                                error=e, request=request, response=response,
                            )
                            ack.response = response

                self._listener_executor.submit(run_ack_function_asynchronously)

            for lazy_func in listener.lazy_functions:
                if request.lazy_function_name:
                    func_name = lazy_func.__name__
                    if func_name == request.lazy_function_name:
                        self.lazy_listener_runner.run(
                            function=lazy_func, request=request
                        )
                        # This HTTP response won't be sent to Slack API servers.
                        return BoltResponse(status=200)
                    else:
                        continue
                else:
                    self._start_lazy_function(lazy_func, request)

            # await for the completion of ack() in the async listener execution
            while ack.response is None and time.time() - starting_time <= 3:
                time.sleep(0.01)

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
        self, lazy_func: Callable[..., None], request: BoltRequest
    ):
        # Start a lazy function asynchronously
        func_name: str = lazy_func.__name__
        self._framework_logger.debug(f"Running lazy listener: {func_name} ...")
        copied_request = self._build_lazy_request(request, func_name)
        self.lazy_listener_runner.start(function=lazy_func, request=copied_request)

    @staticmethod
    def _build_lazy_request(request: BoltRequest, lazy_func_name: str) -> BoltRequest:
        copied_request = create_copy(request)
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
            self._middleware_list.append(
                CustomMiddleware(app_name=self.name, func=func)
            )

    # -------------------------
    # global error handler

    def error(self, func: Callable[..., None]):
        self._listener_error_handler = CustomListenerErrorHandler(
            logger=self._framework_logger, func=func,
        )

    # -------------------------
    # events

    def event(
        self,
        event: Union[str, Pattern, Dict[str, str]],
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
        matchers = matchers if matchers else []
        middleware = middleware if middleware else []

        def __call__(*args, **kwargs):
            functions = self._to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.event("message")
            middleware.append(MessageListenerMatches(keyword))
            return self._register_listener(
                list(functions), primary_matcher, matchers, middleware, True
            )

        return __call__

    # -------------------------
    # slash commands

    def command(
        self,
        command: Union[str, Pattern],
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        matchers: Optional[List[Callable[..., bool]]] = None,
        middleware: Optional[List[Union[Callable, Middleware]]] = None,
    ):
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
        req.context["client"] = self._client

    @staticmethod
    def _to_listener_functions(
        kwargs: dict,
    ) -> Optional[List[Callable[..., Optional[BoltResponse]]]]:
        if kwargs:
            functions = [kwargs["ack"]]
            for sub in kwargs["lazy"]:
                functions.append(sub)
            return functions
        return None

    def _register_listener(
        self,
        functions: List[Callable[..., Optional[BoltResponse]]],
        primary_matcher: ListenerMatcher,
        matchers: Optional[List[Callable[..., bool]]],
        middleware: Optional[List[Union[Callable, Middleware]]],
        auto_acknowledgement: bool = False,
    ) -> None:
        if not isinstance(functions, list):
            functions = list(functions)

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
                raise ValueError(
                    f"Unexpected value for a listener middleware: {type(m)}"
                )

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


# -------------------------


class SlackAppDevelopmentServer:
    def __init__(
        self, port: int, path: str, app: App, oauth_flow: Optional[OAuthFlow] = None,
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

        self._server = HTTPServer(("0.0.0.0", self._port), SlackAppHandler)

    def start(self):
        if self._bolt_app.logger.level > logging.INFO:
            print("⚡️ Bolt app is running! (development server)")
        else:
            self._bolt_app.logger.info("⚡️ Bolt app is running! (development server)")

        try:
            self._server.serve_forever(0.05)
        finally:
            self._server.server_close()
