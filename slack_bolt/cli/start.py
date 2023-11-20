#!/usr/bin/env python
import os
import runpy
import sys

from slack_bolt.app.app import App

from .error import CliError


DEFAULT_ENTRYPOINT_FILE = "app.py"

SLACK_CLI_XOXB = "SLACK_CLI_XOXB"
SLACK_CLI_XAPP = "SLACK_CLI_XAPP"
SLACK_BOT_TOKEN = "SLACK_BOT_TOKEN"
SLACK_APP_TOKEN = "SLACK_APP_TOKEN"


def validate_env() -> None:
    if not os.environ[SLACK_CLI_XOXB]:
        raise CliError(f"Missing local run bot token ({SLACK_CLI_XOXB}). Please see slack-cli maintainers to troubleshoot.")
    if not os.environ[SLACK_CLI_XAPP]:
        raise CliError(f"Missing local run app token ({SLACK_CLI_XAPP}). Please see slack-cli maintainers to troubleshoot.")


def get_entrypoint_path(working_directory: str) -> str:
    custom_path = os.environ.get("SLACK_APP_PATH", None)
    if custom_path:
        return f"{working_directory}/{custom_path}"
    return f"{working_directory}/{DEFAULT_ENTRYPOINT_FILE}"


def load_app_module(entrypoint_path: str) -> str:
    module_name = _get_module_name(entrypoint_path)

    try:
        __import__(module_name)
    except ImportError:
        raise CliError(f"Unable to load module {module_name} found in Entrypoint {entrypoint_path}!")

    module = sys.modules[module_name]

    matches = [v for v in module.__dict__.values() if isinstance(v, App)]

    if len(matches) >= 1:
        return module_name

    raise CliError(f"No Slack App(s) objects detected in module {module_name} from entrypoint {entrypoint_path}")


def _get_module_name(path: str) -> str:
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


def start(working_directory: str) -> None:
    validate_env()

    # TODO improve this to look for the App object in the module then us this file as the entrypoint path
    entrypoint_path = get_entrypoint_path(working_directory)

    if not os.path.exists(entrypoint_path):
        raise CliError(f"Entrypoint not found!\nLooking for: {entrypoint_path}")

    os.environ[SLACK_BOT_TOKEN] = os.environ[SLACK_CLI_XOXB]
    os.environ[SLACK_APP_TOKEN] = os.environ[SLACK_CLI_XAPP]

    try:
        module: str = load_app_module(entrypoint_path)
        runpy.run_module(module)
    finally:
        os.environ.pop(SLACK_BOT_TOKEN, None)
        os.environ.pop(SLACK_APP_TOKEN, None)


if __name__ == "__main__":
    try:
        start(os.getcwd())
    except CliError as e:
        print(e)
        exit()
    except KeyboardInterrupt:
        exit(130)
