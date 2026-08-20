---
sidebar_label: runner
title: slack_bolt.lazy_listener.runner
---

## LazyListenerRunner Objects

```python
class LazyListenerRunner()
```

#### logger: `Logger`

#### start

```python
def start(function: Callable[..., None], request: BoltRequest) -> None
```

Starts a new lazy listener execution.

**Arguments**:

- `function` _Callable[..., None]_ - The function to run.
- `request` _BoltRequest_ - The request to pass to the function. The object must be thread-safe.

#### run

```python
def run(function: Callable[..., None], request: BoltRequest) -> None
```

Synchronously runs the function with a given request data.

**Arguments**:

- `function` _Callable[..., None]_ - The function to run.
- `request` _BoltRequest_ - The request to pass to the function. The object must be thread-safe.
