"""Listeners process incoming requests from Slack.

A listener runs when the request's type or data structure matches its predefined conditions.
Typically, a listener acknowledges the request, processes its data, and may send a response back to Slack.
"""

# Don't add async module imports here
from .custom_listener import CustomListener
from .listener import Listener

builtin_listener_classes = [
    CustomListener,
]
for cls in builtin_listener_classes:
    Listener.register(cls)

__all__ = [
    "CustomListener",
    "Listener",
    "builtin_listener_classes",
]
