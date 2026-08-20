---
sidebar_label: async_handler
title: slack_bolt.adapter.fastapi.async_handler
---

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
