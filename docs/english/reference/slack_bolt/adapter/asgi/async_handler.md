---
sidebar_label: async_handler
title: slack_bolt.adapter.asgi.async_handler
---

## AsyncSlackRequestHandler Objects

```python
class AsyncSlackRequestHandler(SlackRequestHandler)
```

#### app

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

