---
sidebar_label: websocket_client
title: slack_bolt.adapter.socket_mode.websocket_client
---

[`websocket-client`](https://pypi.org/project/websocket-client/) based implementation.

## `SocketModeHandler`

```python
SocketModeHandler(app, app_token=None, logger=None, web_client=None, ping_interval=10, concurrency=10, http_proxy_host=None, http_proxy_port=None, http_proxy_auth=None, proxy_type=None, trace_enabled=False)
```

Bases: BaseSocketModeHandler

Socket Mode adapter for Bolt apps.

**Parameters:**

- **app** (App) – The Bolt app
- **app_token** (Optional[str]) – App-level token starting with `xapp-`
- **logger** (Optional[Logger]) – Custom logger
- **web_client** (Optional[WebClient]) – custom `slack_sdk.web.WebClient` instance
- **ping_interval** (float) – The ping-pong internal (seconds)
- **concurrency** (int) – The size of the underlying thread pool
- **http_proxy_host** (Optional[str]) – HTTP proxy host
- **http_proxy_port** (Optional[int]) – HTTP proxy port
- **http_proxy_auth** (Optional[Tuple[str, str]]) – HTTP proxy authentication (username, password)
- **proxy_type** (Optional[str]) – Proxy type
- **trace_enabled** (bool) – True if trace-level logging is enabled

### `close`

```python
close()
```

Disconnects from the Socket Mode server and cleans the resources this instance holds up.

### `connect`

```python
connect()
```

Establishes a new connection with the Socket Mode server.

### `disconnect`

```python
disconnect()
```

Disconnects the current WebSocket connection with the Socket Mode server.

### `start`

```python
start()
```

Establishes a new connection and then blocks the current thread to prevent the termination of this process.

If you don't want to block the current thread, use `#connect()` method instead.
