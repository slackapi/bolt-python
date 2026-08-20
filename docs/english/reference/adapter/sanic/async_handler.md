---
sidebar_label: async_handler
title: slack_bolt.adapter.sanic.async_handler
---

#### to\_async\_bolt\_request

```python
def to_async_bolt_request(
    req: Request,
    addition_context_properties: Optional[Dict[str, Any]] = None) -> AsyncBoltRequest
```

#### to\_sanic\_response

```python
def to_sanic_response(bolt_resp: BoltResponse) -> HTTPResponse
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
    addition_context_properties: Optional[Dict[str, Any]] = None) -> HTTPResponse
```
