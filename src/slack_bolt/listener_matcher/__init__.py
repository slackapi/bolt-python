# Don't add async module imports here
from .custom_listener_matcher import CustomListenerMatcher
from .listener_matcher import ListenerMatcher

builtin_listener_matcher_classes = [
    CustomListenerMatcher,
]
for cls in builtin_listener_matcher_classes:
    ListenerMatcher.register(cls)
