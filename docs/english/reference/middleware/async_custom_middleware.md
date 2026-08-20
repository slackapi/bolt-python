---
sidebar_label: async_custom_middleware
title: slack_bolt.middleware.async_custom_middleware
---

## AsyncCustomMiddleware Objects

```python
class AsyncCustomMiddleware(AsyncMiddleware)
```

#### app\_name: `str`

#### func: `Callable[..., Awaitable[Any]]`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(
    *,
    app_name: str,
    func: Callable[..., Awaitable[Any]],
    base_logger: Optional[Logger] = None)
```

#### async\_process

```python
async def async_process(
    *,
    req: AsyncBoltRequest,
    resp: BoltResponse,
    next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```

#### name

```python
@property
def name() -> str
```
