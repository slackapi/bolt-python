---
sidebar_label: socket_mode
title: slack_bolt.adapter.socket_mode
---

Socket Mode adapter package provides the following implementations. If you don't have strong reasons to use 3rd party library based adapters, we recommend using the built-in client based one.

* `slack_bolt.adapter.socket_mode.builtin`
* `slack_bolt.adapter.socket_mode.websocket_client`
* `slack_bolt.adapter.socket_mode.aiohttp`
* `slack_bolt.adapter.socket_mode.websockets`

## Submodules

- [slack_bolt.adapter.socket_mode.aiohttp](/tools/bolt-python/reference/adapter/socket_mode/aiohttp)
- [slack_bolt.adapter.socket_mode.async_base_handler](/tools/bolt-python/reference/adapter/socket_mode/async_base_handler)
- [slack_bolt.adapter.socket_mode.async_handler](/tools/bolt-python/reference/adapter/socket_mode/async_handler)
- [slack_bolt.adapter.socket_mode.async_internals](/tools/bolt-python/reference/adapter/socket_mode/async_internals)
- [slack_bolt.adapter.socket_mode.base_handler](/tools/bolt-python/reference/adapter/socket_mode/base_handler)
- [slack_bolt.adapter.socket_mode.builtin](/tools/bolt-python/reference/adapter/socket_mode/builtin)
- [slack_bolt.adapter.socket_mode.internals](/tools/bolt-python/reference/adapter/socket_mode/internals)
- [slack_bolt.adapter.socket_mode.websocket_client](/tools/bolt-python/reference/adapter/socket_mode/websocket_client)
- [slack_bolt.adapter.socket_mode.websockets](/tools/bolt-python/reference/adapter/socket_mode/websockets)

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
    proxy: Optional[str] = None,
    proxy_headers: Optional[Dict[str, str]] = None,
    auto_reconnect_enabled: bool = True,
    trace_enabled: bool = False,
    all_message_trace_enabled: bool = False,
    ping_pong_trace_enabled: bool = False,
    ping_interval: float = 10,
    receive_buffer_size: int = 1024,
    concurrency: int = 10)
```

Socket Mode adapter for Bolt apps.

**Arguments**:

- `app` _App_ - The Bolt app
- `app_token` _Optional[str]_ - App-level token starting with `xapp-`
- `logger` _Optional[Logger]_ - Custom logger
- `web_client` _Optional[WebClient]_ - custom `slack_sdk.web.WebClient` instance
- `proxy` _Optional[str]_ - HTTP proxy URL
- `proxy_headers` _Optional[Dict[str, str]]_ - Additional request header for proxy connections
- `auto_reconnect_enabled` _bool_ - True if the auto-reconnect logic works
- `trace_enabled` _bool_ - True if trace-level logging is enabled
- `all_message_trace_enabled` _bool_ - True if trace-logging for all received WebSocket messages is enabled
- `ping_pong_trace_enabled` _bool_ - True if trace-logging for all ping-pong communications
- `ping_interval` _float_ - The ping-pong internal (seconds)
- `receive_buffer_size` _int_ - The data length for a single socket recv operation
- `concurrency` _int_ - The size of the underlying thread pool

#### handle

```python
def handle(client: SocketModeClient, req: SocketModeRequest) -> None
```
