---
sidebar_label: async_runner
title: slack_bolt.lazy_listener.async_runner
---

## AsyncLazyListenerRunner Objects

```python
class AsyncLazyListenerRunner()
```

#### logger: `Logger`

#### start

```python
def start(function: Callable[..., Awaitable[None]], request: AsyncBoltRequest) -> None
```

Starts a new lazy listener execution.

**Arguments**:

- `function` _Callable[..., Awaitable[None]]_ - The function to run.
- `request` _AsyncBoltRequest_ - The request to pass to the function. The object must be thread-safe.

#### run

```python
async def run(
    function: Callable[..., Awaitable[None]],
    request: AsyncBoltRequest) -> None
```

Synchronously run the function with a given request data.

**Arguments**:

- `function` _Callable[..., Awaitable[None]]_ - The function to run.
- `request` _AsyncBoltRequest_ - The request to pass to the function. The object must be thread-safe.
