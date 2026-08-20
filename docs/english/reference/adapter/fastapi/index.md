---
sidebar_label: fastapi
title: slack_bolt.adapter.fastapi
---

## Submodules

- [slack_bolt.adapter.fastapi.async_handler](/tools/bolt-python/reference/adapter/fastapi/async_handler)

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
