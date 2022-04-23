"""A middleware processes request data and calls `next()` method
if the execution chain should continue running the following middleware.

Middleware can be used globally before all listener executions.
It's also possible to run a middleware only for a particular listener.
"""

# Don't add async module imports here
from .authorization import (
    SingleTeamAuthorization,
    MultiTeamsAuthorization,
)  # noqa: F401
from .custom_middleware import CustomMiddleware  # noqa: F401
from .ignoring_self_events import IgnoringSelfEvents  # noqa: F401
from .middleware import Middleware  # noqa: F401
from .request_verification import RequestVerification  # noqa: F401
from .ssl_check import SslCheck  # noqa: F401
from .url_verification import UrlVerification  # noqa: F401

builtin_middleware_classes = [
    SslCheck,
    RequestVerification,
    SingleTeamAuthorization,
    MultiTeamsAuthorization,
    IgnoringSelfEvents,
    UrlVerification,
]
for cls in builtin_middleware_classes:
    Middleware.register(cls)
