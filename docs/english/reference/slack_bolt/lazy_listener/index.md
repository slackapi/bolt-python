---
sidebar_label: lazy_listener
title: slack_bolt.lazy_listener
---

Lazy listener runner is a beta feature for the apps running on Function-as-a-Service platforms.

```python
    def respond_to_slack_within_3_seconds(body, ack):
        text = body.get("text")
        if text is None or len(text) == 0:
            ack(f":x: Usage: /start-process (description here)")
        else:
            ack(f"Accepted! (task: {body['text']})")

    import time
    def run_long_process(respond, body):
        time.sleep(5)  # longer than 3 seconds
        respond(f"Completed! (task: {body['text']})")

    app.command("/start-process")(
        # ack() is still called within 3 seconds
        ack=respond_to_slack_within_3_seconds,
        # Lazy function is responsible for processing the event
        lazy=[run_long_process]
    )
```

Refer to https://docs.slack.dev/tools/bolt-python/concepts/lazy-listeners for more details.

## LazyListenerRunner Objects

```python
class LazyListenerRunner(metaclass=ABCMeta)
```

#### logger

#### start

```python
@abstractmethod
def start(function: Callable[..., None], request: BoltRequest) -> None
```

Starts a new lazy listener execution.

**Arguments**:

- `function` - The function to run.
- `request` - The request to pass to the function. The object must be thread-safe.

#### run

```python
def run(function: Callable[..., None], request: BoltRequest) -> None
```

Synchronously runs the function with a given request data.

**Arguments**:

- `function` - The function to run.
- `request` - The request to pass to the function. The object must be thread-safe.

## ThreadLazyListenerRunner Objects

```python
class ThreadLazyListenerRunner(LazyListenerRunner)
```

#### logger

#### \_\_init\_\_

```python
def __init__(logger: Logger, executor: Executor)
```

#### start

```python
def start(function: Callable[..., None], request: BoltRequest) -> None
```

