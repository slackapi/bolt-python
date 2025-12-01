"""All listeners have access to a context dictionary, which can be used to enrich events with additional information.
Bolt automatically attaches information that is included in the incoming event,
like `user_id`, `team_id`, `channel_id`, and `enterprise_id`.

Refer to https://docs.slack.dev/tools/bolt-python/concepts/context for details.
"""

# Don't add async module imports here
from .context import BoltContext

__all__ = [
    "BoltContext",
]
