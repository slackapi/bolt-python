---
sidebar_label: base_handler
title: slack_bolt.adapter.asgi.base_handler
---

## BaseSlackRequestHandler Objects

```python
class BaseSlackRequestHandler()
```

#### app: `Union[App, AsyncApp]`

#### path: `str`

#### dispatch

```python
async def dispatch(request: AsgiHttpRequest) -> BoltResponse
```

Dispatches a request to the Bolt App

#### handle\_installation

```python
async def handle_installation(request: AsgiHttpRequest) -> BoltResponse
```

Handles installation of the OAuthFlow

#### handle\_callback

```python
async def handle_callback(request: AsgiHttpRequest) -> BoltResponse
```

Handles the callback of the OAuthFlow
