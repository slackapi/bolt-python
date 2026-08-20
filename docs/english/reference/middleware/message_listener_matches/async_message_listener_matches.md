---
sidebar_label: async_message_listener_matches
title: slack_bolt.middleware.message_listener_matches.async_message_listener_matches
---

## AsyncMessageListenerMatches Objects

```python
class AsyncMessageListenerMatches(AsyncMiddleware)
```

#### \_\_init\_\_

```python
def __init__(keyword: Union[str, Pattern])
```

Captures matched keywords and saves the values in context.

#### async\_process

```python
async def async_process(
    *,
    req: AsyncBoltRequest,
    resp: BoltResponse,
    next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```
