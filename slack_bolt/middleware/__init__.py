# Don't add async module imports here
from .authorization import SingleTeamAuthorization, MultiTeamsAuthorization
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
