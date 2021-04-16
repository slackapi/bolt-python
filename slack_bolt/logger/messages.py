import time
from typing import Union

from slack_sdk.web import SlackResponse

from slack_bolt.request import BoltRequest


# -------------------------------
# Error
# -------------------------------


def error_client_invalid_type() -> str:
    return "`client` must be a slack_sdk.web.WebClient"


def error_client_invalid_type_async() -> str:
    return "`client` must be a slack_sdk.web.async_client.AsyncWebClient"


def error_oauth_flow_invalid_type_async() -> str:
    return "`oauth_flow` must be a slack_bolt.oauth.async_oauth_flow.AsyncOAuthFlow"


def error_oauth_settings_invalid_type_async() -> str:
    return "`oauth_settings` must be a slack_bolt.oauth.async_oauth_settings.AsyncOAuthSettings"


def error_auth_test_failure(error_response: SlackResponse) -> str:
    return f"`token` is invalid (auth.test result: {error_response})"


def error_token_required() -> str:
    return (
        "Either an env variable `SLACK_BOT_TOKEN` "
        "or `token` argument in the constructor is required."
    )


def error_unexpected_listener_middleware(middleware_type) -> str:
    return f"Unexpected value for a listener middleware: {middleware_type}"


def error_listener_function_must_be_coro_func(func_name: str) -> str:
    return f"The listener function ({func_name}) is not a coroutine function."


def error_authorize_conflicts() -> str:
    return "`authorize` in the top-level arguments is not allowed when you pass either `oauth_settings` or `oauth_flow`"


def error_message_event_type(event_type: str) -> str:
    return (
        f'Although the document mentions "{event_type}", '
        'it is not a valid event type. Use "message" instead. '
        "If you want to filter message events, you can use `event.channel_type` for it."
    )


def error_installation_store_required_for_builtin_listeners() -> str:
    return (
        "To use the event listeners for token revocation handling, "
        "setting a valid `installation_store` to `App`/`AsyncApp` is required."
    )


# -------------------------------
# Warning
# -------------------------------


def warning_client_prioritized_and_token_skipped() -> str:
    return "As you gave `client` as well, `token` will be unused."


def warning_token_skipped() -> str:
    return (
        "As `installation_store` or `authorize` has been used, "
        "`token` (or SLACK_BOT_TOKEN env variable) will be ignored."
    )


def warning_installation_store_conflicts() -> str:
    return "As you gave both `installation_store` and `oauth_settings`/`auth_flow`, the top level one is unused."


def warning_unhandled_by_global_middleware(  # type: ignore
    name: str, req: Union[BoltRequest, "AsyncBoltRequest"]  # type: ignore
) -> str:  # type: ignore
    return (
        f"A global middleware ({name}) skipped calling `next()` "
        f"without providing a response for the request ({req.body})"
    )


def warning_unhandled_request(  # type: ignore
    req: Union[BoltRequest, "AsyncBoltRequest"],  # type: ignore
) -> str:  # type: ignore
    return f"Unhandled request ({req.body})"


def warning_did_not_call_ack(listener_name: str) -> str:
    return f"{listener_name} didn't call ack()"


def warning_bot_only_conflicts() -> str:
    return (
        "installation_store_bot_only exists in both App and OAuthFlow.settings. "
        "The one passed in App constructor is used."
    )


def warning_skip_uncommon_arg_name(arg_name: str) -> str:
    return (
        f"Bolt skips injecting a value to the first keyword argument ({arg_name}). "
        "If it is self/cls of a method, we recommend using the common names."
    )


# -------------------------------
# Info
# -------------------------------


def info_default_oauth_settings_loaded() -> str:
    return (
        "As you've set SLACK_CLIENT_ID and SLACK_CLIENT_SECRET env variables, "
        "Bolt has enabled the file-based InstallationStore/OAuthStateStore for you. "
        "Note that these file-based stores are for local development. "
        "If you'd like to use a different data store, set the oauth_settings argument in the App constructor. "
        "Please refer to https://slack.dev/bolt-python/concepts#authenticating-oauth for more details."
    )


# -------------------------------
# Debug
# -------------------------------


def debug_applying_middleware(middleware_name: str) -> str:
    return f"Applying {middleware_name}"


def debug_checking_listener(listener_name: str) -> str:
    return f"Checking listener: {listener_name} ..."


def debug_running_listener(listener_name: str) -> str:
    return f"Running listener: {listener_name} ..."


def debug_running_lazy_listener(func_name: str) -> str:
    return f"Running lazy listener: {func_name} ..."


def debug_responding(status: int, body: str, millis: int) -> str:
    return f'Responding with status: {status} body: "{body}" ({millis} millis)'


def debug_return_listener_middleware_response(
    listener_name: str, status: int, body: str, starting_time: float
) -> str:
    millis = int((time.time() - starting_time) * 1000)
    return f"Responding with listener middleware's response - listener: {listener_name}, status: {status}, body: {body} ({millis} millis)"
