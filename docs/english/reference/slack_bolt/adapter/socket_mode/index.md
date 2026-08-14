---
sidebar_label: socket_mode
title: slack_bolt.adapter.socket_mode
---

Socket Mode adapter package provides the following implementations. If you don&#x27;t have strong reasons to use 3rd party library based adapters, we recommend using the built-in client based one.

* `slack_bolt.adapter.socket_mode.builtin`
* `slack_bolt.adapter.socket_mode.websocket_client`
* `slack_bolt.adapter.socket_mode.aiohttp`
* `slack_bolt.adapter.socket_mode.websockets`

## SocketModeHandler Objects

```python
class SocketModeHandler(BaseSocketModeHandler)
```

#### app

#### app\_token

#### client

#### \_\_init\_\_

```python
def __init__(app: App,
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

Socket Mode adapter for Bolt apps

**Arguments**:

- `app` - The Bolt app
- `app_token` - App-level token starting with `xapp-`
- `logger` - Custom logger
- `web_client` - custom `slack_sdk.web.WebClient` instance
- `proxy` - HTTP proxy URL
- `proxy_headers` - Additional request header for proxy connections
- `auto_reconnect_enabled` - True if the auto-reconnect logic works
- `trace_enabled` - True if trace-level logging is enabled
- `all_message_trace_enabled` - True if trace-logging for all received WebSocket messages is enabled
- `ping_pong_trace_enabled` - True if trace-logging for all ping-pong communications
- `ping_interval` - The ping-pong internal (seconds)
- `receive_buffer_size` - The data length for a single socket recv operation
- `concurrency` - The size of the underlying thread pool

#### handle

```python
def handle(client: SocketModeClient, req: SocketModeRequest) -> None
```

