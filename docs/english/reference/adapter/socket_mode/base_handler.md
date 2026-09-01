---
sidebar_label: base_handler
title: slack_bolt.adapter.socket_mode.base_handler
---

The base class of Socket Mode client implementation.

If you want to build asyncio-based ones, use `AsyncBaseSocketModeHandler` instead.

## `BaseSocketModeHandler`

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

### `handle`

```python
handle(client, req)
```

Handles Socket Mode envelope requests through a WebSocket connection.

**Parameters:**

- **client** (BaseSocketModeClient) – this Socket Mode client instance
- **req** (SocketModeRequest) – the request data

### `start`

```python
start()
```

Establishes a new connection and then blocks the current thread to prevent the termination of this process.

If you don't want to block the current thread, use `#connect()` method instead.
