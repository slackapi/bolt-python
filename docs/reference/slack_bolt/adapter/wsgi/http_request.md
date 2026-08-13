---
sidebar_label: http_request
title: slack_bolt.adapter.wsgi.http_request
---

## WsgiHttpRequest Objects

```python
class WsgiHttpRequest()
```

This Class uses the PEP 3333 standard to extract request information
from the WSGI web server running the application

PEP 3333: https://peps.python.org/pep-3333/

#### get\_headers

```python
def get_headers() -> Dict[str, Union[str, Sequence[str]]]
```

#### get\_body

```python
def get_body() -> str
```

