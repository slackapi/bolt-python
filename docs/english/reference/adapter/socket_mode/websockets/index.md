---
sidebar_label: websockets
title: slack_bolt.adapter.socket_mode.websockets
---

[`websockets`](https://pypi.org/project/websockets/) based implementation  / asyncio compatible

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
    ping_interval: float = 10)
```

Socket Mode adapter for Bolt apps.

Please note that this adapter does not support proxy configuration
as the underlying websockets module does not support proxy-wired connections.
If you use proxy, consider using one of the other Socket Mode adapters.

**Arguments**:

- `app` _App_ - The Bolt app
- `app_token` _Optional[str]_ - App-level token starting with `xapp-`
- `logger` _Optional[Logger]_ - Custom logger
- `web_client` _Optional[AsyncWebClient]_ - custom `slack_sdk.web.WebClient` instance
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
    ping_interval: float = 10)
```

#### handle

```python
async def handle(client: SocketModeClient, req: SocketModeRequest) -> None
```
