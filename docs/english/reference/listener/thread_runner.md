---
sidebar_label: thread_runner
title: slack_bolt.listener.thread_runner
---

## ThreadListenerRunner Objects

```python
class ThreadListenerRunner()
```

#### logger: `Logger`

#### process\_before\_response: `bool`

#### listener\_error\_handler: `ListenerErrorHandler`

#### listener\_start\_handler: `ListenerStartHandler`

#### listener\_completion\_handler: `ListenerCompletionHandler`

#### listener\_executor: `Executor`

#### lazy\_listener\_runner: `LazyListenerRunner`

#### \_\_init\_\_

```python
def __init__(
    logger: Logger,
    process_before_response: bool,
    listener_error_handler: ListenerErrorHandler,
    listener_start_handler: ListenerStartHandler,
    listener_completion_handler: ListenerCompletionHandler,
    listener_executor: Executor,
    lazy_listener_runner: LazyListenerRunner)
```

#### run

```python
def run(
    request: BoltRequest,
    response: BoltResponse,
    listener_name: str,
    listener: Listener,
    starting_time: Optional[float] = None) -> Optional[BoltResponse]
```
