---
sidebar_label: handler
title: slack_bolt.adapter.google_cloud_functions.handler
---

## NoopLazyListenerRunner Objects

```python
class NoopLazyListenerRunner(LazyListenerRunner)
```

#### start

```python
def start(function: Callable[..., None], request: BoltRequest) -> None
```

## SlackRequestHandler Objects

```python
class SlackRequestHandler()
```

#### \_\_init\_\_

```python
def __init__(app: App)
```

#### handle

```python
def handle(req: Request) -> Response
```
