---
sidebar_label: listener_completion_handler
title: slack_bolt.listener.listener_completion_handler
---

## ListenerCompletionHandler Objects

```python
class ListenerCompletionHandler()
```

#### handle

```python
def handle(request: BoltRequest, response: Optional[BoltResponse]) -> None
```

Do something extra after the listener execution.

**Arguments**:

- `request` _BoltRequest_ - The request.
- `response` _Optional[BoltResponse]_ - The response.

## CustomListenerCompletionHandler Objects

```python
class CustomListenerCompletionHandler(ListenerCompletionHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger, func: Callable[..., None])
```

#### handle

```python
def handle(request: BoltRequest, response: Optional[BoltResponse])
```

## DefaultListenerCompletionHandler Objects

```python
class DefaultListenerCompletionHandler(ListenerCompletionHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger)
```

#### handle

```python
def handle(request: BoltRequest, response: Optional[BoltResponse])
```
