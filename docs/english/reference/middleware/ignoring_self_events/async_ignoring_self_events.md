---
sidebar_label: async_ignoring_self_events
title: slack_bolt.middleware.ignoring_self_events.async_ignoring_self_events
---

## AsyncIgnoringSelfEvents Objects

```python
class AsyncIgnoringSelfEvents(IgnoringSelfEvents, AsyncMiddleware)
```

#### async\_process

```python
async def async_process(
    *,
    req: AsyncBoltRequest,
    resp: BoltResponse,
    next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```
