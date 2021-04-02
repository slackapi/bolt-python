import logging
from logging import Logger
from threading import current_thread, Thread
from typing import Optional, Callable

from django.http import HttpRequest, HttpResponse

from slack_bolt.app import App
from slack_bolt.error import BoltError
from slack_bolt.lazy_listener import ThreadLazyListenerRunner
from slack_bolt.lazy_listener.internals import build_runnable_function
from slack_bolt.listener.listener_completion_handler import (
    ListenerCompletionHandler,
    DefaultListenerCompletionHandler,
)
from slack_bolt.listener.thread_runner import ThreadListenerRunner
from slack_bolt.oauth import OAuthFlow
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


def to_bolt_request(req: HttpRequest) -> BoltRequest:
    raw_body: bytes = req.body
    body: str = raw_body.decode("utf-8") if raw_body else ""
    return BoltRequest(
        body=body,
        query=req.META["QUERY_STRING"],
        headers=req.headers,
    )


def to_django_response(bolt_resp: BoltResponse) -> HttpResponse:
    resp: HttpResponse = HttpResponse(
        status=bolt_resp.status,
        content=bolt_resp.body.encode("utf-8"),
    )
    for k, v in bolt_resp.first_headers_without_set_cookie().items():
        resp[k] = v

    for cookie in bolt_resp.cookies():
        for name, c in cookie.items():
            str_max_age: Optional[str] = c.get("max-age")
            max_age: Optional[int] = int(str_max_age) if str_max_age else None
            resp.set_cookie(
                key=name,
                value=c.value,
                expires=c.get("expires"),
                max_age=max_age,
                domain=c.get("domain"),
                path=c.get("path"),
                secure=True,
                httponly=True,
            )
    return resp


from django.db import connections


def release_thread_local_connections(logger: Logger, execution_type: str):
    connections.close_all()
    if logger.level <= logging.DEBUG:
        current: Thread = current_thread()
        logger.debug(
            f"Released thread-bound DB connections (thread name: {current.name}, execution type: {execution_type})"
        )


class DjangoListenerCompletionHandler(ListenerCompletionHandler):
    """Django sets DB connections as a thread-local variable per thread.
    If the thread is not managed on the Django app side, the connections won't be released by Django.
    This handler releases the connections every time a ThreadListenerRunner execution completes.
    """

    def handle(self, request: BoltRequest, response: Optional[BoltResponse]) -> None:
        release_thread_local_connections(request.context.logger, "listener")


class DjangoThreadLazyListenerRunner(ThreadLazyListenerRunner):
    def start(self, function: Callable[..., None], request: BoltRequest) -> None:
        func: Callable[[], None] = build_runnable_function(
            func=function,
            logger=self.logger,
            request=request,
        )

        def wrapped_func():
            try:
                func()
            finally:
                release_thread_local_connections(
                    request.context.logger, "lazy-listener"
                )

        self.executor.submit(wrapped_func)


class SlackRequestHandler:
    def __init__(self, app: App):  # type: ignore
        self.app = app
        listener_runner = self.app.listener_runner
        # This runner closes all thread-local connections in the thread when an execution completes
        self.app.listener_runner.lazy_listener_runner = DjangoThreadLazyListenerRunner(
            logger=listener_runner.logger,
            executor=listener_runner.listener_executor,
        )

        if not isinstance(listener_runner, ThreadListenerRunner):
            raise BoltError(
                "Custom listener_runners are not compatible with this Django adapter."
            )

        if app.process_before_response is True:
            # As long as the app access Django models in the same thread,
            # Django cleans the connections up for you.
            self.app.logger.debug("App.process_before_response is set to True")
            return

        current_completion_handler = listener_runner.listener_completion_handler
        if current_completion_handler is not None and not isinstance(
            current_completion_handler, DefaultListenerCompletionHandler
        ):
            message = """As you've already set app.listener_runner.listener_completion_handler to your own one,
            Bolt skipped to set it to slack_sdk.adapter.django.DjangoListenerCompletionHandler.
            We strongly recommend having the following lines of code in your listener_completion_handler:

            from django.db import connections
            connections.close_all()
            """
            self.app.logger.warning(message)
            return
        # for proper management of thread-local Django DB connections
        self.app.listener_runner.listener_completion_handler = (
            DjangoListenerCompletionHandler()
        )
        self.app.logger.debug("DjangoListenerCompletionHandler has been enabled")

    def handle(self, req: HttpRequest) -> HttpResponse:
        if req.method == "GET":
            if self.app.oauth_flow is not None:
                oauth_flow: OAuthFlow = self.app.oauth_flow
                if req.path == oauth_flow.install_path:
                    bolt_resp = oauth_flow.handle_installation(to_bolt_request(req))
                    return to_django_response(bolt_resp)
                elif req.path == oauth_flow.redirect_uri_path:
                    bolt_resp = oauth_flow.handle_callback(to_bolt_request(req))
                    return to_django_response(bolt_resp)
        elif req.method == "POST":
            bolt_resp: BoltResponse = self.app.dispatch(to_bolt_request(req))
            return to_django_response(bolt_resp)

        return HttpResponse(status=404, content=b"Not Found")
