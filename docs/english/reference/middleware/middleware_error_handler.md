---
sidebar_label: middleware_error_handler
title: slack_bolt.middleware.middleware_error_handler
---

## MiddlewareErrorHandler Objects

```python
class MiddlewareErrorHandler()
```

#### handle

```python
def handle(
    error: Exception,
    request: BoltRequest,
    response: Optional[BoltResponse]) -> None
```

Handles an unhandled exception.

**Arguments**:

- `error` _Exception_ - The raised exception.
- `request` _BoltRequest_ - The request.
- `response` _Optional[BoltResponse]_ - The response.

## CustomMiddlewareErrorHandler Objects

```python
class CustomMiddlewareErrorHandler(MiddlewareErrorHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger, func: Callable[..., Optional[BoltResponse]])
```

#### handle

```python
def handle(error: Exception, request: BoltRequest, response: Optional[BoltResponse])
```

## DefaultMiddlewareErrorHandler Objects

```python
class DefaultMiddlewareErrorHandler(MiddlewareErrorHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger)
```

#### handle

```python
def handle(error: Exception, request: BoltRequest, response: Optional[BoltResponse])
```
