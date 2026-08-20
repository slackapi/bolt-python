---
sidebar_label: async_handler
title: slack_bolt.adapter.asgi.async_handler
---

## AsyncSlackRequestHandler Objects

```python
class AsyncSlackRequestHandler(SlackRequestHandler)
```

#### app: `AsyncApp`

#### \_\_init\_\_

```python
def __init__(app: AsyncApp, path: str = '/slack/events')
```

Setup Bolt as an ASGI web framework, this will make your application compatible with ASGI web servers.
This can be used for production deployment.

With the default settings, `http://localhost:3000/slack/events`
Run Bolt with [uvicron](https://www.uvicorn.org/)

    # Python
    app = AsyncApp()
    api = SlackRequestHandler(app)

    # bash
    export SLACK_SIGNING_SECRET=***
    export SLACK_BOT_TOKEN=xoxb-***
    uvicorn app:api --port 3000 --log-level debug

**Arguments**:

- `app` _AsyncApp_ - Your bolt application
- `path` _str_ - The path to handle request from Slack (Default: `/slack/events`)

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
