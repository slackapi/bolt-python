---
sidebar_label: async_ssl_check
title: slack_bolt.middleware.ssl_check.async_ssl_check
---

## AsyncSslCheck Objects

```python
class AsyncSslCheck(SslCheck, AsyncMiddleware)
```

#### async\_process

```python
async def async_process(
    *,
    req: AsyncBoltRequest,
    resp: BoltResponse,
    next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```
