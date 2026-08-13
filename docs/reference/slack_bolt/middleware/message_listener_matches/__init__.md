---
sidebar_label: message_listener_matches
title: slack_bolt.middleware.message_listener_matches
---

## MessageListenerMatches Objects

```python
class MessageListenerMatches(Middleware)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

