---
sidebar_label: base_handler
title: slack_bolt.adapter.socket_mode.base_handler
---

The base class of Socket Mode client implementation.
If you want to build asyncio-based ones, use `AsyncBaseSocketModeHandler` instead.

## BaseSocketModeHandler Objects

```python
class BaseSocketModeHandler()
```

#### app: `App`

#### client: `BaseSocketModeClient`

#### handle

```python
def handle(client: BaseSocketModeClient, req: SocketModeRequest) -> None
```

Handles Socket Mode envelope requests through a WebSocket connection.

**Arguments**:

- `client` _BaseSocketModeClient_ - this Socket Mode client instance
- `req` _SocketModeRequest_ - the request data

#### connect

```python
def connect()
```

Establishes a new connection with the Socket Mode server

#### disconnect

```python
def disconnect()
```

Disconnects the current WebSocket connection with the Socket Mode server

#### close

```python
def close()
```

Disconnects from the Socket Mode server and cleans the resources this instance holds up

#### start

```python
def start()
```

Establishes a new connection and then blocks the current thread
to prevent the termination of this process.
If you don't want to block the current thread, use `#connect()` method instead.
