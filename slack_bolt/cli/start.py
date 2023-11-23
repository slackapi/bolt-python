#!/usr/bin/env python
import os
import runpy

from .error import CliError

from .protocol import Protocol, protocol_factory

PROTOCOL: Protocol

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


def start(working_directory: str) -> None:
    validate_env()

    entrypoint_path = get_entrypoint_path(working_directory)

    if not os.path.exists(entrypoint_path):
        raise CliError(f"Entrypoint not found!\nLooking for: {entrypoint_path}")

    os.environ[SLACK_BOT_TOKEN] = os.environ[SLACK_CLI_XOXB]
    os.environ[SLACK_APP_TOKEN] = os.environ[SLACK_CLI_XAPP]

    try:
        runpy.run_path(entrypoint_path, run_name="__main__")
    finally:
        os.environ.pop(SLACK_BOT_TOKEN, None)
        os.environ.pop(SLACK_APP_TOKEN, None)


if __name__ == "__main__":
    PROTOCOL = protocol_factory()
    start(os.getcwd())
