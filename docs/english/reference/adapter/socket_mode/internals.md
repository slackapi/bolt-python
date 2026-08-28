---
sidebar_label: internals
title: slack_bolt.adapter.socket_mode.internals
---

Internal functions.

#### build\_headers

```python
def build_headers(
    req: SocketModeRequest) -> Optional[Dict[str, Union[str, Sequence[str]]]]
```

#### run\_bolt\_app

```python
def run_bolt_app(app: App, req: SocketModeRequest)
```

#### send\_response

```python
def send_response(
    client: BaseSocketModeClient,
    req: SocketModeRequest,
    bolt_resp: BoltResponse,
    start_time: float)
```
