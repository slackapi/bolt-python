from .async_middleware import AsyncMiddleware
from .authorization import \
    SingleTeamAuthorization, \
    MultiTeamsAuthorization, \
    AsyncSingleTeamAuthorization, \
    AsyncMultiTeamsAuthorization
from .custom_middleware import CustomMiddleware
from .ignoring_self_events import IgnoringSelfEvents
from .middleware import Middleware
from .request_verification import RequestVerification
from .ssl_check import SslCheck
from .url_verification import UrlVerification

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

builtin_async_middleware_classes = [
    SslCheck,
    RequestVerification,
    AsyncSingleTeamAuthorization,
    AsyncMultiTeamsAuthorization,
    IgnoringSelfEvents,
    UrlVerification,
]
for cls in builtin_async_middleware_classes:
    AsyncMiddleware.register(cls)
