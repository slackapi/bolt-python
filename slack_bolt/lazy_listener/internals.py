import inspect
from functools import wraps
from logging import Logger
from typing import Callable

from slack_bolt.kwargs_injection import build_required_kwargs
from slack_bolt.request import BoltRequest


def build_runnable_function(
    func: Callable[..., None],
    logger: Logger,
    request: BoltRequest,
) -> Callable[[], None]:
    arg_names = inspect.getfullargspec(func).args

    @wraps(func)
    def request_wired_func_wrapper() -> None:
        try:
            func(
                **build_required_kwargs(
                    logger=logger,
                    required_arg_names=arg_names,
                    request=request,
                    response=None,
                    this_func=func,
                )
            )
        except Exception as e:
            logger.error(f"Failed to run an internal function ({e})")

    return request_wired_func_wrapper
