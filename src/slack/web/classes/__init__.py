from slack_sdk.models import (
    BaseObject,
    JsonObject,
    JsonValidator,
    EnumValidator,
)  # noqa
from slack_sdk.models import extract_json, show_unknown_key_warning  # noqa

from slack import deprecation

deprecation.show_message(__name__, "slack_sdk.models")
