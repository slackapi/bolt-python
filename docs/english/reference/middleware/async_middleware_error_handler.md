---
sidebar_label: async_middleware_error_handler
title: slack_bolt.middleware.async_middleware_error_handler
---

## AsyncMiddlewareErrorHandler Objects

```python
class AsyncMiddlewareErrorHandler()
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

## AsyncCustomMiddlewareErrorHandler Objects

```python
class AsyncCustomMiddlewareErrorHandler(AsyncMiddlewareErrorHandler)
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

## AsyncDefaultMiddlewareErrorHandler Objects

```python
class AsyncDefaultMiddlewareErrorHandler(AsyncMiddlewareErrorHandler)
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
