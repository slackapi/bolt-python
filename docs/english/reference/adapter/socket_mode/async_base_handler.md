---
sidebar_label: async_base_handler
title: slack_bolt.adapter.socket_mode.async_base_handler
---

The base class of asyncio-based Socket Mode client implementation.

## AsyncBaseSocketModeHandler Objects

```python
class AsyncBaseSocketModeHandler()
```

#### app: `Union[App, AsyncApp]`

#### client: `AsyncBaseSocketModeClient`

#### handle

```python
async def handle(client: AsyncBaseSocketModeClient, req: SocketModeRequest) -> None
```

Handles Socket Mode envelope requests through a WebSocket connection.

**Arguments**:

- `client` _AsyncBaseSocketModeClient_ - this Socket Mode client instance
- `req` _SocketModeRequest_ - the request data

#### connect\_async

```python
async def connect_async()
```

Establishes a new connection with the Socket Mode server.

#### disconnect\_async

```python
async def disconnect_async()
```

Disconnects the current WebSocket connection with the Socket Mode server.

#### close\_async

```python
async def close_async()
```

Disconnects from the Socket Mode server and cleans the resources this instance holds up.

#### start\_async

```python
async def start_async()
```

Establishes a new connection and then starts infinite sleep to prevent the termination of this process.

If you don't want to have the sleep, use `#connect()` method instead.
