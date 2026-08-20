---
sidebar_label: asyncio_runner
title: slack_bolt.lazy_listener.asyncio_runner
---

## AsyncioLazyListenerRunner Objects

```python
class AsyncioLazyListenerRunner(AsyncLazyListenerRunner)
```

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(logger: Logger)
```

#### start

```python
def start(function: Callable[..., Awaitable[None]], request: AsyncBoltRequest) -> None
```
