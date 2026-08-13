---
sidebar_label: async_handler
title: slack_bolt.adapter.socket_mode.async_handler
---

Default implementation is the aiohttp-based one.

## AsyncSocketModeHandler Objects

```python
class AsyncSocketModeHandler(AsyncBaseSocketModeHandler)
```

#### app

#### app\_token

#### client

#### handle

```python
async def handle(client: SocketModeClient, req: SocketModeRequest) -> None
```

