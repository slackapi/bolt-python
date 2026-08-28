---
sidebar_label: socket_mode
title: slack_bolt.adapter.socket_mode
---

Socket Mode adapter package provides the following implementations. If you don't have strong reasons to use 3rd party library based adapters, we recommend using the built-in client based one.

* `slack_bolt.adapter.socket_mode.builtin`
* `slack_bolt.adapter.socket_mode.websocket_client`
* `slack_bolt.adapter.socket_mode.aiohttp`
* `slack_bolt.adapter.socket_mode.websockets`

## `SocketModeHandler`

```python
SocketModeHandler(app, app_token=None, logger=None, web_client=None, proxy=None, proxy_headers=None, auto_reconnect_enabled=True, trace_enabled=False, all_message_trace_enabled=False, ping_pong_trace_enabled=False, ping_interval=10, receive_buffer_size=1024, concurrency=10)
```

Bases: BaseSocketModeHandler

Socket Mode adapter for Bolt apps.

**Parameters:**

- **app** (App) – The Bolt app
- **app_token** (Optional[str]) – App-level token starting with `xapp-`
- **logger** (Optional[Logger]) – Custom logger
- **web_client** (Optional[WebClient]) – custom `slack_sdk.web.WebClient` instance
- **proxy** (Optional[str]) – HTTP proxy URL
- **proxy_headers** (Optional[Dict[str, str]]) – Additional request header for proxy connections
- **auto_reconnect_enabled** (bool) – True if the auto-reconnect logic works
- **trace_enabled** (bool) – True if trace-level logging is enabled
- **all_message_trace_enabled** (bool) – True if trace-logging for all received WebSocket messages is enabled
- **ping_pong_trace_enabled** (bool) – True if trace-logging for all ping-pong communications
- **ping_interval** (float) – The ping-pong internal (seconds)
- **receive_buffer_size** (int) – The data length for a single socket recv operation
- **concurrency** (int) – The size of the underlying thread pool

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
