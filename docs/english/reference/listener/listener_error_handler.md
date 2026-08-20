---
sidebar_label: listener_error_handler
title: slack_bolt.listener.listener_error_handler
---

## ListenerErrorHandler Objects

```python
class ListenerErrorHandler()
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

## CustomListenerErrorHandler Objects

```python
class CustomListenerErrorHandler(ListenerErrorHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger, func: Callable[..., Optional[BoltResponse]])
```

#### handle

```python
def handle(error: Exception, request: BoltRequest, response: Optional[BoltResponse])
```

## DefaultListenerErrorHandler Objects

```python
class DefaultListenerErrorHandler(ListenerErrorHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger)
```

#### handle

```python
def handle(error: Exception, request: BoltRequest, response: Optional[BoltResponse])
```
