---
sidebar_label: async_runner
title: slack_bolt.lazy_listener.async_runner
---

## `AsyncLazyListenerRunner`

### `run`

```python
run(function, request)
```

Synchronously run the function with a given request data.

**Parameters:**

- **function** (Callable..., [Awaitable[None]]) – The function to run.
- **request** (AsyncBoltRequest) – The request to pass to the function. The object must be thread-safe.

### `start`

```python
start(function, request)
```

Starts a new lazy listener execution.

**Parameters:**

- **function** (Callable..., [Awaitable[None]]) – The function to run.
- **request** (AsyncBoltRequest) – The request to pass to the function. The object must be thread-safe.
