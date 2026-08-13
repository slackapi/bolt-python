---
sidebar_label: socket_mode
title: slack_bolt.adapter.socket_mode
---

Socket Mode adapter package provides the following implementations. If you don&#x27;t have strong reasons to use 3rd party library based adapters, we recommend using the built-in client based one.

* `slack_bolt.adapter.socket_mode.builtin`
* `slack_bolt.adapter.socket_mode.websocket_client`
* `slack_bolt.adapter.socket_mode.aiohttp`
* `slack_bolt.adapter.socket_mode.websockets`

## SocketModeHandler Objects

```python
class SocketModeHandler(BaseSocketModeHandler)
```

#### app

#### app\_token

#### client

#### handle

```python
def handle(client: SocketModeClient, req: SocketModeRequest) -> None
```

