from slack_bolt.middleware.authorization import SingleTeamAuthorization, MultiTeamsAuthorization
from slack_bolt.middleware.custom_middleware import CustomMiddleware
from slack_bolt.middleware.ignoring_self_events import IgnoringSelfEvents
from slack_bolt.middleware.middleware import Middleware
from slack_bolt.middleware.request_verification import RequestVerification
from slack_bolt.middleware.ssl_check import SslCheck
from slack_bolt.middleware.url_verification import UrlVerification

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
