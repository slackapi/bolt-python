# Don't add async module imports here
from .custom_listener import CustomListener
from .listener import Listener

builtin_listener_classes = [
    CustomListener,
]
for cls in builtin_listener_classes:
    Listener.register(cls)
