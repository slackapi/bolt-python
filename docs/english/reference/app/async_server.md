---
sidebar_label: async_server
title: slack_bolt.app.async_server
---

## AsyncSlackAppServer Objects

```python
class AsyncSlackAppServer()
```

#### port: `int`

#### path: `str`

#### host: `str`

#### bolt\_app: `AsyncApp`

#### web\_app: `web.Application`

#### \_\_init\_\_

```python
def __init__(port: int, path: str, app: AsyncApp, host: Optional[str] = None)
```

Standalone AIOHTTP Web Server.

Refer to https://docs.aiohttp.org/en/stable/web.html for details of AIOHTTP.

**Arguments**:

- `port` _int_ - The port to listen on
- `path` _str_ - The path to receive incoming requests from Slack
- `app` _AsyncApp_ - The `AsyncApp` instance that is used for processing requests
- `host` _Optional[str]_ - The hostname to serve the web endpoints. (Default: 0.0.0.0)

#### handle\_get\_requests

```python
async def handle_get_requests(request: web.Request) -> web.Response
```

#### handle\_post\_requests

```python
async def handle_post_requests(request: web.Request) -> web.Response
```

#### start

```python
def start(host: Optional[str] = None) -> None
```

Starts a new web server process.
