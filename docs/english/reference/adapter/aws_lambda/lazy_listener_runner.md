---
sidebar_label: lazy_listener_runner
title: slack_bolt.adapter.aws_lambda.lazy_listener_runner
---

## LambdaLazyListenerRunner Objects

```python
class LambdaLazyListenerRunner(LazyListenerRunner)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger, lambda_client: Optional[Any] = None)
```

#### start

```python
def start(function: Callable[..., None], request: BoltRequest) -> None
```
