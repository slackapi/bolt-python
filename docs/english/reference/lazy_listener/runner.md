---
sidebar_label: runner
title: slack_bolt.lazy_listener.runner
---

## `LazyListenerRunner`

### `run`

```python
run(function, request)
```

Synchronously runs the function with a given request data.

**Parameters:**

- **function** (Callable[..., None]) – The function to run.
- **request** (BoltRequest) – The request to pass to the function. The object must be thread-safe.

### `start`

```python
start(function, request)
```

Starts a new lazy listener execution.

**Parameters:**

- **function** (Callable[..., None]) – The function to run.
- **request** (BoltRequest) – The request to pass to the function. The object must be thread-safe.
