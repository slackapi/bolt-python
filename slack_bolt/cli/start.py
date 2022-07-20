#!/usr/bin/env python
import os
import subprocess
from .hook_utils.errors import handle_exception, CliError


DEFAULT_ENTRYPOINT_FILE = "app.py"

SLACK_CLI_XOXB = "SLACK_CLI_XOXB"
SLACK_CLI_XAPP = "SLACK_CLI_XAPP"


def validate_env():
    if not os.environ[SLACK_CLI_XOXB]:
        raise CliError("Missing local run bot token. Please see slack-cli maintainers to troubleshoot.")
    if not os.environ[SLACK_CLI_XAPP]:
        raise CliError("Missing local run app token. Please see slack-cli maintainers to troubleshoot.")


def get_entrypoint_path(working_directory):
    custom_path = os.environ.get("SLACK_CLI_CUSTOM_FILE_PATH", None)
    if custom_path:
        return f"{working_directory}/{custom_path}"
    return f"{working_directory}/{DEFAULT_ENTRYPOINT_FILE}"


def execute_process(command, env):
    with subprocess.Popen(command, env=env, stdout=subprocess.PIPE,
                          universal_newlines=True, bufsize=1) as app_process:
        for line in app_process.stdout:
            yield line


@handle_exception
def start(working_directory):
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


def main():
    current_wd = os.getcwd()
    start(current_wd)
