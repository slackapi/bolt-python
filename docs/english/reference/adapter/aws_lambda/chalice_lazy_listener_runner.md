---
sidebar_label: chalice_lazy_listener_runner
title: slack_bolt.adapter.aws_lambda.chalice_lazy_listener_runner
---

## ChaliceLazyListenerRunner Objects

```python
class ChaliceLazyListenerRunner(LazyListenerRunner)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger, lambda_client: Optional[BaseClient] = None)
```

#### start

```python
def start(function: Callable[..., None], request: BoltRequest) -> None
```
