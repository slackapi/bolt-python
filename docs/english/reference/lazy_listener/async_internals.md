---
sidebar_label: async_internals
title: slack_bolt.lazy_listener.async_internals
---

#### to\_runnable\_function

```python
async def to_runnable_function(
    internal_func: Callable[..., Awaitable[None]],
    logger: Logger,
    request: AsyncBoltRequest)
```
