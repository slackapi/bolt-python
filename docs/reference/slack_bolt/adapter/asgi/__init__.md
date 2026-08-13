---
sidebar_label: asgi
title: slack_bolt.adapter.asgi
---

## SlackRequestHandler Objects

```python
class SlackRequestHandler(BaseSlackRequestHandler)
```

#### dispatch

```python
async def dispatch(request: AsgiHttpRequest) -> BoltResponse
```

#### handle\_installation

```python
async def handle_installation(request: AsgiHttpRequest) -> BoltResponse
```

#### handle\_callback

```python
async def handle_callback(request: AsgiHttpRequest) -> BoltResponse
```

