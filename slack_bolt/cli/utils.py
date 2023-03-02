import os
import sys
from slack_bolt import App
from ..error import CliError
from typing import Callable, Any


def handle_exceptions() -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except CliError as e:
                print(e)
                exit()
            except KeyboardInterrupt:
                exit(130)

        return wrapper

    return decorator


def load_app(entrypoint_path: str) -> App:

    module_name = get_module_name(entrypoint_path)

    try:
        __import__(module_name)
    except ImportError:
        raise CliError(f"Unable to load module {module_name} found in Entrypoint {entrypoint_path}!")

    module = sys.modules[module_name]

    matches = [v for v in module.__dict__.values() if isinstance(v, App)]

    if len(matches) == 1:
        app = matches[0]
    else:
        raise CliError(
            f"Detected {len(matches)} Slack App(s) objects in module {module_name} from entrypoint {entrypoint_path}"
        )

    if not app:
        CliError(f"Entrypoint {entrypoint_path} does not contain an App object!")

    return app


def get_module_name(path: str) -> str:
    path = os.path.realpath(path)

    fname, ext = os.path.splitext(path)
    if ext == ".py":
        path = fname

    if os.path.basename(path) == "__init__":
        path = os.path.dirname(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join(path, "__init__.py")):
            break

    if sys.path[0] != path:
        sys.path.insert(0, path)

    return ".".join(module_name[::-1])
