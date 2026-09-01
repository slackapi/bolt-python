---
sidebar_label: aiohttp
title: slack_bolt.adapter.socket_mode.aiohttp
---

[`aiohttp`](https://pypi.org/project/aiohttp/) based implementation / asyncio compatible.

## `SocketModeHandler`

```python
SocketModeHandler(app, app_token=None, logger=None, web_client=None, proxy=None, ping_interval=10)
```

Bases: AsyncBaseSocketModeHandler

Socket Mode adapter for Bolt apps.

**Parameters:**

- **app** (App) – The Bolt app
- **app_token** (Optional[str]) – App-level token starting with `xapp-`
- **logger** (Optional[Logger]) – Custom logger
- **web_client** (Optional[AsyncWebClient]) – custom `slack_sdk.web.WebClient` instance
- **proxy** (Optional[str]) – HTTP proxy URL
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
