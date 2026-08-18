---
sidebar_label: message_listener_matches
title: slack_bolt.middleware.message_listener_matches
---

## Submodules

- [slack_bolt.middleware.message_listener_matches.async_message_listener_matches](/tools/bolt-python/reference/middleware/message_listener_matches/async_message_listener_matches)
- [slack_bolt.middleware.message_listener_matches.message_listener_matches](/tools/bolt-python/reference/middleware/message_listener_matches/message_listener_matches)

## MessageListenerMatches Objects

```python
class MessageListenerMatches(Middleware)
```

#### \_\_init\_\_

```python
def __init__(keyword: Union[str, Pattern])
```

Captures matched keywords and saves the values in context.

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

