---
sidebar_label: sanic
title: slack_bolt.adapter.sanic
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
    addition_context_properties: Optional[Dict[str,
                                               Any]] = None) -> HTTPResponse
```

