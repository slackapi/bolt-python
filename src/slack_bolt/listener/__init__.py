from .custom_listener import CustomListener
from .listener import Listener
from .url_verification import UrlVerificationListener

builtin_listener_classes = [
    CustomListener,
    UrlVerificationListener,
]
for cls in builtin_listener_classes:
    Listener.register(cls)
