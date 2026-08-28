---
sidebar_label: async_listener_completion_handler
title: slack_bolt.listener.async_listener_completion_handler
---

## AsyncListenerCompletionHandler Objects

```python
class AsyncListenerCompletionHandler()
```

#### handle

```python
async def handle(request: AsyncBoltRequest, response: Optional[BoltResponse]) -> None
```

Do something extra after the listener execution.

**Arguments**:

- `request` _AsyncBoltRequest_ - The request.
- `response` _Optional[BoltResponse]_ - The response.

## AsyncCustomListenerCompletionHandler Objects

```python
class AsyncCustomListenerCompletionHandler(AsyncListenerCompletionHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger, func: Callable[..., Awaitable[None]])
```

#### handle

```python
async def handle(request: AsyncBoltRequest, response: Optional[BoltResponse]) -> None
```

## AsyncDefaultListenerCompletionHandler Objects

```python
class AsyncDefaultListenerCompletionHandler(AsyncListenerCompletionHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger)
```

#### handle

```python
async def handle(request: AsyncBoltRequest, response: Optional[BoltResponse])
```
