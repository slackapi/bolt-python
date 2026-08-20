---
sidebar_label: async_handler
title: slack_bolt.adapter.starlette.async_handler
---

#### to\_async\_bolt\_request

```python
def to_async_bolt_request(
    req: Request,
    body: bytes,
    addition_context_properties: Optional[Dict[str, Any]] = None) -> AsyncBoltRequest
```

#### to\_starlette\_response

```python
def to_starlette_response(bolt_resp: BoltResponse) -> Response
```

## AsyncSlackRequestHandler Objects

```python
class AsyncSlackRequestHandler()
```

#### \_\_init\_\_

```python
def __init__(app: AsyncApp)
```

#### handle

```python
async def handle(
    req: Request,
    addition_context_properties: Optional[Dict[str, Any]] = None) -> Response
```
