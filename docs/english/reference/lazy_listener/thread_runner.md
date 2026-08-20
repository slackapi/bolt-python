---
sidebar_label: thread_runner
title: slack_bolt.lazy_listener.thread_runner
---

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
