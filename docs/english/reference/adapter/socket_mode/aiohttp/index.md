---
sidebar_label: aiohttp
title: slack_bolt.adapter.socket_mode.aiohttp
---

[`aiohttp`](https://pypi.org/project/aiohttp/) based implementation / asyncio compatible

## SocketModeHandler Objects

```python
class SocketModeHandler(AsyncBaseSocketModeHandler)
```

#### app: `App`

#### app\_token: `str`

#### client: `SocketModeClient`

#### \_\_init\_\_

```python
def __init__(
    app: App,
    app_token: Optional[str] = None,
    logger: Optional[Logger] = None,
    web_client: Optional[AsyncWebClient] = None,
    proxy: Optional[str] = None,
    ping_interval: float = 10)
```

Socket Mode adapter for Bolt apps

**Arguments**:

- `app` _App_ - The Bolt app
- `app_token` _Optional[str]_ - App-level token starting with `xapp-`
- `logger` _Optional[Logger]_ - Custom logger
- `web_client` _Optional[AsyncWebClient]_ - custom `slack_sdk.web.WebClient` instance
- `proxy` _Optional[str]_ - HTTP proxy URL
- `ping_interval` _float_ - The ping-pong internal (seconds)

#### handle

```python
async def handle(client: SocketModeClient, req: SocketModeRequest) -> None
```

## AsyncSocketModeHandler Objects

```python
class AsyncSocketModeHandler(AsyncBaseSocketModeHandler)
```

#### app: `AsyncApp`

#### app\_token: `str`

#### client: `SocketModeClient`

#### \_\_init\_\_

```python
def __init__(
    app: AsyncApp,
    app_token: Optional[str] = None,
    logger: Optional[Logger] = None,
    web_client: Optional[AsyncWebClient] = None,
    proxy: Optional[str] = None,
    ping_interval: float = 10,
    loop: Optional[AbstractEventLoop] = None)
```

#### handle

```python
async def handle(client: SocketModeClient, req: SocketModeRequest) -> None
```
