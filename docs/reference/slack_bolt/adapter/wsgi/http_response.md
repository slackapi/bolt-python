---
sidebar_label: http_response
title: slack_bolt.adapter.wsgi.http_response
---

## WsgiHttpResponse Objects

```python
class WsgiHttpResponse()
```

This Class uses the PEP 3333 standard to adapt bolt response information
for the WSGI web server running the application

PEP 3333: https://peps.python.org/pep-3333/

#### get\_headers

```python
def get_headers() -> List[Tuple[str, str]]
```

#### get\_body

```python
def get_body() -> Iterable[bytes]
```

