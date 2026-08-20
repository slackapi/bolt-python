---
sidebar_label: http_request
title: slack_bolt.adapter.asgi.http_request
---

## AsgiHttpRequest Objects

```python
class AsgiHttpRequest()
```

#### \_\_init\_\_

```python
def __init__(scope: scope_type, receive: Callable)
```

#### raw\_headers: `Iterable[Tuple[bytes, bytes]]`

#### get\_headers

```python
def get_headers() -> Dict[str, Union[str, Sequence[str]]]
```

#### get\_raw\_body

```python
async def get_raw_body() -> str
```
