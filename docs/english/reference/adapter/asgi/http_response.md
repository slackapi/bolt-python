---
sidebar_label: http_response
title: slack_bolt.adapter.asgi.http_response
---

## AsgiHttpResponse Objects

```python
class AsgiHttpResponse()
```

#### \_\_init\_\_

```python
def __init__(status: int,
             headers: Dict[str, Sequence[str]] = {},
             body: str = "")
```

#### get\_response\_start

```python
def get_response_start(
) -> Dict[str, Union[str, int, Iterable[Tuple[bytes, bytes]]]]
```

#### get\_response\_body

```python
def get_response_body() -> Dict[str, Union[str, bytes, bool]]
```

