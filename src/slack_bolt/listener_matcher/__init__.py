from .async_custom_listener_matcher import AsyncCustomListenerMatcher
from .async_listener_matcher import AsyncListenerMatcher
from .custom_listener_matcher import CustomListenerMatcher
from .listener_matcher import ListenerMatcher

builtin_listener_matcher_classes = [
    CustomListenerMatcher,
]
for cls in builtin_listener_matcher_classes:
    ListenerMatcher.register(cls)

builtin_async_listener_matcher_classes = [
    AsyncCustomListenerMatcher,
]
for cls in builtin_async_listener_matcher_classes:
    AsyncListenerMatcher.register(cls)
