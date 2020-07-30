from .async_custom_listener import AsyncCustomListener
from .async_listener import AsyncListener
from .custom_listener import CustomListener
from .listener import Listener

builtin_listener_classes = [
    CustomListener,
]
for cls in builtin_listener_classes:
    Listener.register(cls)

builtin_async_listener_classes = [
    AsyncCustomListener,
]
for cls in builtin_async_listener_classes:
    AsyncListener.register(cls)
