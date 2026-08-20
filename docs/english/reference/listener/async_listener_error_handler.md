---
sidebar_label: async_listener_error_handler
title: slack_bolt.listener.async_listener_error_handler
---

## AsyncListenerErrorHandler Objects

```python
class AsyncListenerErrorHandler()
```

#### handle

```python
async def handle(
    error: Exception,
    request: AsyncBoltRequest,
    response: Optional[BoltResponse]) -> None
```

Handles an unhandled exception.

**Arguments**:

- `error` _Exception_ - The raised exception.
- `request` _AsyncBoltRequest_ - The request.
- `response` _Optional[BoltResponse]_ - The response.

## AsyncCustomListenerErrorHandler Objects

```python
class AsyncCustomListenerErrorHandler(AsyncListenerErrorHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger, func: Callable[..., Awaitable[Optional[BoltResponse]]])
```

#### handle

```python
async def handle(
    error: Exception,
    request: AsyncBoltRequest,
    response: Optional[BoltResponse]) -> None
```

## AsyncDefaultListenerErrorHandler Objects

```python
class AsyncDefaultListenerErrorHandler(AsyncListenerErrorHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger)
```

#### handle

```python
async def handle(
    error: Exception,
    request: AsyncBoltRequest,
    response: Optional[BoltResponse])
```
