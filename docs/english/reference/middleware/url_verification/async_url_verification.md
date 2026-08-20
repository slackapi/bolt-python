---
sidebar_label: async_url_verification
title: slack_bolt.middleware.url_verification.async_url_verification
---

## AsyncUrlVerification Objects

```python
class AsyncUrlVerification(UrlVerification, AsyncMiddleware)
```

#### \_\_init\_\_

```python
def __init__(base_logger: Optional[Logger] = None)
```

#### async\_process

```python
async def async_process(
    *,
    req: AsyncBoltRequest,
    resp: BoltResponse,
    next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```
