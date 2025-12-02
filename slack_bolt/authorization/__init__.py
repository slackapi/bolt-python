"""Authorization is the process of determining which Slack credentials should be available
while processing an incoming Slack event.

Refer to https://docs.slack.dev/tools/bolt-python/concepts/authorization for details.
"""

from .authorize_result import AuthorizeResult

__all__ = [
    "AuthorizeResult",
]
