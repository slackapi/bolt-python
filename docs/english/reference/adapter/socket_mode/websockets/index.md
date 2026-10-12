---
sidebar_label: websockets
title: slack_bolt.adapter.socket_mode.websockets
---

[`websockets`](https://pypi.org/project/websockets/) based implementation  / asyncio compatible.

## `SocketModeHandler`

```python
SocketModeHandler(app, app_token=None, logger=None, web_client=None, ping_interval=10)
```

Bases: AsyncBaseSocketModeHandler

Socket Mode adapter for Bolt apps.

Please note that this adapter does not support proxy configuration
as the underlying websockets module does not support proxy-wired connections.
If you use proxy, consider using one of the other Socket Mode adapters.

**Parameters:**

- **app** (App) – The Bolt app
- **app_token** (Optional[str]) – App-level token starting with `xapp-`
- **logger** (Optional[Logger]) – Custom logger
- **web_client** (Optional[AsyncWebClient]) – custom `slack_sdk.web.WebClient` instance
- **ping_interval** (float) – The ping-pong internal (seconds)

### `close_async`

```python
close_async()
```

Disconnects from the Socket Mode server and cleans the resources this instance holds up.

### `connect_async`

```python
connect_async()
```

Establishes a new connection with the Socket Mode server.

### `disconnect_async`

```python
disconnect_async()
```

Disconnects the current WebSocket connection with the Socket Mode server.

### `start_async`

```python
start_async()
```

Establishes a new connection and then starts infinite sleep to prevent the termination of this process.

If you don't want to have the sleep, use `#connect()` method instead.
