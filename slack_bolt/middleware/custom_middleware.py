import inspect
from logging import Logger
from typing import Callable, Any, Sequence

from slack_bolt.kwargs_injection import build_required_kwargs
from slack_bolt.logger import get_bolt_app_logger
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from .middleware import Middleware
from slack_bolt.util.utils import get_name_for_callable


class CustomMiddleware(Middleware):
    app_name: str
    func: Callable[..., Any]
    arg_names: Sequence[str]
    logger: Logger

    def __init__(self, *, app_name: str, func: Callable):
        self.app_name = app_name
        self.func = func
        self.arg_names = inspect.getfullargspec(func).args
        self.logger = get_bolt_app_logger(self.app_name, self.func)

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        return self.func(
            **build_required_kwargs(
                logger=self.logger,
                required_arg_names=self.arg_names,
                request=req,
                response=resp,
                next_func=next,
                this_func=self.func,
            )
        )

    @property
    def name(self) -> str:
        return f"CustomMiddleware(func={get_name_for_callable(self.func)})"
