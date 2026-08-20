---
sidebar_label: async_attaching_function_token
title: slack_bolt.middleware.attaching_function_token.async_attaching_function_token
---

## AsyncAttachingFunctionToken Objects

```python
class AsyncAttachingFunctionToken(AsyncMiddleware)
```

#### async\_process

```python
async def async_process(
    *,
    req: AsyncBoltRequest,
    resp: BoltResponse,
    next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```
