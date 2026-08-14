---
sidebar_label: starlette
title: slack_bolt.adapter.starlette
---

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
        addition_context_properties: Optional[Dict[str,
                                                   Any]] = None) -> Response
```

