---
sidebar_label: asyncio_runner
title: slack_bolt.listener.asyncio_runner
---

## AsyncioListenerRunner Objects

```python
class AsyncioListenerRunner()
```

#### logger: `Logger`

#### process\_before\_response: `bool`

#### listener\_error\_handler: `AsyncListenerErrorHandler`

#### listener\_start\_handler: `AsyncListenerStartHandler`

#### listener\_completion\_handler: `AsyncListenerCompletionHandler`

#### lazy\_listener\_runner: `AsyncLazyListenerRunner`

#### \_\_init\_\_

```python
def __init__(
    logger: Logger,
    process_before_response: bool,
    listener_error_handler: AsyncListenerErrorHandler,
    listener_start_handler: AsyncListenerStartHandler,
    listener_completion_handler: AsyncListenerCompletionHandler,
    lazy_listener_runner: AsyncLazyListenerRunner)
```

#### run

```python
async def run(
    request: AsyncBoltRequest,
    response: BoltResponse,
    listener_name: str,
    listener: AsyncListener,
    starting_time: Optional[float] = None) -> Optional[BoltResponse]
```
