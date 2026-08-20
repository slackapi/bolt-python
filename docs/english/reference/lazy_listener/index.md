---
sidebar_label: lazy_listener
title: slack_bolt.lazy_listener
---

## Submodules

- [slack_bolt.lazy_listener.async_internals](/tools/bolt-python/reference/lazy_listener/async_internals)
- [slack_bolt.lazy_listener.async_runner](/tools/bolt-python/reference/lazy_listener/async_runner)
- [slack_bolt.lazy_listener.asyncio_runner](/tools/bolt-python/reference/lazy_listener/asyncio_runner)
- [slack_bolt.lazy_listener.internals](/tools/bolt-python/reference/lazy_listener/internals)
- [slack_bolt.lazy_listener.runner](/tools/bolt-python/reference/lazy_listener/runner)
- [slack_bolt.lazy_listener.thread_runner](/tools/bolt-python/reference/lazy_listener/thread_runner)

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

## ThreadLazyListenerRunner Objects

```python
class ThreadLazyListenerRunner(LazyListenerRunner)
```

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(logger: Logger, executor: Executor)
```

#### start

```python
def start(function: Callable[..., None], request: BoltRequest) -> None
```
