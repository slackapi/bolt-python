---
sidebar_label: custom_middleware
title: slack_bolt.middleware.custom_middleware
---

## CustomMiddleware Objects

```python
class CustomMiddleware(Middleware)
```

#### app\_name: `str`

#### func: `Callable[..., Any]`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(*, app_name: str, func: Callable, base_logger: Optional[Logger] = None)
```

#### process

```python
def process(
    *,
    req: BoltRequest,
    resp: BoltResponse,
    next: Callable[[], BoltResponse]) -> BoltResponse
```

#### name

```python
@property
def name() -> str
```
