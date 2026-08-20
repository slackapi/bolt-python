---
sidebar_label: async_handler
title: slack_bolt.adapter.socket_mode.async_handler
---

## AsyncSocketModeHandler Objects

```python
class AsyncSocketModeHandler(AsyncBaseSocketModeHandler)
```

#### app: `AsyncApp`

#### app\_token: `str`

#### client: `SocketModeClient`

#### \_\_init\_\_

```python
def __init__(
    app: AsyncApp,
    app_token: Optional[str] = None,
    logger: Optional[Logger] = None,
    web_client: Optional[AsyncWebClient] = None,
    proxy: Optional[str] = None,
    ping_interval: float = 10,
    loop: Optional[AbstractEventLoop] = None)
```

#### handle

```python
async def handle(client: SocketModeClient, req: SocketModeRequest) -> None
```
