---
sidebar_label: http_response
title: slack_bolt.adapter.wsgi.http_response
---

## WsgiHttpResponse Objects

```python
class WsgiHttpResponse()
```

Adapts bolt response information for the WSGI web server using the PEP 3333 standard.

PEP 3333: https://peps.python.org/pep-3333/

#### \_\_init\_\_

```python
def __init__(
    status: int,
    headers: Optional[Dict[str, Sequence[str]]] = None,
    body: str = '')
```

#### get\_headers

```python
def get_headers() -> List[Tuple[str, str]]
```

#### get\_body

```python
def get_body() -> Iterable[bytes]
```
