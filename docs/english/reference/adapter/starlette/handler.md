---
sidebar_label: handler
title: slack_bolt.adapter.starlette.handler
---

#### to\_bolt\_request

```python
def to_bolt_request(
    req: Request,
    body: bytes,
    addition_context_properties: Optional[Dict[str, Any]] = None) -> BoltRequest
```

#### to\_starlette\_response

```python
def to_starlette_response(bolt_resp: BoltResponse) -> Response
```

## SlackRequestHandler Objects

```python
class SlackRequestHandler()
```

#### \_\_init\_\_

```python
def __init__(app: App)
```

#### handle

```python
async def handle(
    req: Request,
    addition_context_properties: Optional[Dict[str, Any]] = None) -> Response
```
