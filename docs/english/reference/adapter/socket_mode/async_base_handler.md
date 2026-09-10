---
sidebar_label: async_base_handler
title: slack_bolt.adapter.socket_mode.async_base_handler
---

The base class of asyncio-based Socket Mode client implementation.

## `AsyncBaseSocketModeHandler`

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

### `handle`

```python
handle(client, req)
```

Handles Socket Mode envelope requests through a WebSocket connection.

**Parameters:**

- **client** (AsyncBaseSocketModeClient) – this Socket Mode client instance
- **req** (SocketModeRequest) – the request data

### `start_async`

```python
start_async()
```

Establishes a new connection and then starts infinite sleep to prevent the termination of this process.

If you don't want to have the sleep, use `#connect()` method instead.
