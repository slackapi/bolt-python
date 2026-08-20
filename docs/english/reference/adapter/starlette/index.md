---
sidebar_label: starlette
title: slack_bolt.adapter.starlette
---

## Submodules

- [slack_bolt.adapter.starlette.async_handler](/tools/bolt-python/reference/adapter/starlette/async_handler)
- [slack_bolt.adapter.starlette.handler](/tools/bolt-python/reference/adapter/starlette/handler)

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
