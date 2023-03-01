#!/usr/bin/env python
import os
import sys
import subprocess
from slack_bolt import App
from typing import List, Generator
from ..error import CliError
from .utils import handle_exception


DEFAULT_ENTRYPOINT_FILE = "app.py"

SLACK_CLI_XOXB = "SLACK_CLI_XOXB"
SLACK_CLI_XAPP = "SLACK_CLI_XAPP"


def validate_env() -> None:
    if not os.environ[SLACK_CLI_XOXB]:
        raise CliError(f"Missing local run bot token ({SLACK_CLI_XOXB}). Please see slack-cli maintainers to troubleshoot.")
    if not os.environ[SLACK_CLI_XAPP]:
        raise CliError(f"Missing local run app token ({SLACK_CLI_XAPP}). Please see slack-cli maintainers to troubleshoot.")


def get_entrypoint_path(working_directory: str) -> str:
    custom_path = os.environ.get("SLACK_CLI_CUSTOM_FILE_PATH", None)
    if custom_path:
        return f"{working_directory}/{custom_path}"
    return f"{working_directory}/{DEFAULT_ENTRYPOINT_FILE}"


def load_app(entrypoint_path) -> App:
    """Loads the Flask app (if not yet loaded) and returns it.  Calling
    this multiple times will just result in the already loaded app to
    be returned.
    """
    if not os.path.exists(entrypoint_path):
        raise CliError(f"Entrypoint not found!\nLooking for: {entrypoint_path}")

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
            f"Detected multiple or no Slack App objects in module {module_name} from entrypoint {entrypoint_path}"
        )

    if not app:
        CliError(f"Entrypoint {entrypoint_path} does not contain an App object!")

    return app


def get_module_name(path):
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


def execute_process(command: List[str], env: dict) -> Generator[str, None, None]:
    with subprocess.Popen(command, env=env, stdout=subprocess.PIPE, universal_newlines=True, bufsize=1) as app_process:
        for line in app_process.stdout:
            yield line


@handle_exception()
def start(working_directory: str) -> None:
    validate_env()

    entrypoint_path = get_entrypoint_path(working_directory)
    print(f"Entrypoint path:\n{entrypoint_path}")

    if not os.path.exists(entrypoint_path):
        raise CliError(f"Entrypoint not found!\nLooking for: {entrypoint_path}")

    local_env = dict(os.environ)
    local_env["SLACK_BOT_TOKEN"] = os.environ[SLACK_CLI_XOXB]
    local_env["SLACK_APP_TOKEN"] = os.environ[SLACK_CLI_XAPP]

    command = ["python", "-u", entrypoint_path]

    for stdout in execute_process(command, local_env):
        print(stdout, end="")


if __name__ == "__main__":
    current_wd = os.getcwd()
    start(current_wd)
