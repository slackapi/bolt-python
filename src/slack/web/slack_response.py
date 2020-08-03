from slack import deprecation
from slack_sdk.web.legacy_slack_response import (
    LegacySlackResponse as SlackResponse,
)  # noqa

deprecation.show_message(__name__, "slack_sdk.web.slack_response")
