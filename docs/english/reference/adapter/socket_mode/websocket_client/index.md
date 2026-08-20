---
sidebar_label: websocket_client
title: slack_bolt.adapter.socket_mode.websocket_client
---

[`websocket-client`](https://pypi.org/project/websocket-client/) based implementation

## SocketModeHandler Objects

```python
class SocketModeHandler(BaseSocketModeHandler)
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
    web_client: Optional[WebClient] = None,
    ping_interval: float = 10,
    concurrency: int = 10,
    http_proxy_host: Optional[str] = None,
    http_proxy_port: Optional[int] = None,
    http_proxy_auth: Optional[Tuple[str, str]] = None,
    proxy_type: Optional[str] = None,
    trace_enabled: bool = False)
```

Socket Mode adapter for Bolt apps

**Arguments**:

- `app` _App_ - The Bolt app
- `app_token` _Optional[str]_ - App-level token starting with `xapp-`
- `logger` _Optional[Logger]_ - Custom logger
- `web_client` _Optional[WebClient]_ - custom `slack_sdk.web.WebClient` instance
- `ping_interval` _float_ - The ping-pong internal (seconds)
- `concurrency` _int_ - The size of the underlying thread pool
- `http_proxy_host` _Optional[str]_ - HTTP proxy host
- `http_proxy_port` _Optional[int]_ - HTTP proxy port
- `http_proxy_auth` _Optional[Tuple[str, str]]_ - HTTP proxy authentication (username, password)
- `proxy_type` _Optional[str]_ - Proxy type
- `trace_enabled` _bool_ - True if trace-level logging is enabled

#### handle

```python
def handle(client: SocketModeClient, req: SocketModeRequest) -> None
```
