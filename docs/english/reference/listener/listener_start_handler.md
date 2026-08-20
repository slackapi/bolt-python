---
sidebar_label: listener_start_handler
title: slack_bolt.listener.listener_start_handler
---

## ListenerStartHandler Objects

```python
class ListenerStartHandler()
```

#### handle

```python
def handle(request: BoltRequest, response: Optional[BoltResponse]) -> None
```

Do something extra before the listener execution.

This handler is useful if a developer needs to maintain/clean up
thread-local resources such as Django ORM database connections
before a listener execution starts.

**Arguments**:

- `request` _BoltRequest_ - The request.
- `response` _Optional[BoltResponse]_ - The response.

## CustomListenerStartHandler Objects

```python
class CustomListenerStartHandler(ListenerStartHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger, func: Callable[..., None])
```

#### handle

```python
def handle(request: BoltRequest, response: Optional[BoltResponse])
```

## DefaultListenerStartHandler Objects

```python
class DefaultListenerStartHandler(ListenerStartHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger)
```

#### handle

```python
def handle(request: BoltRequest, response: Optional[BoltResponse])
```
