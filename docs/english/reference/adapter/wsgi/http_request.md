---
sidebar_label: http_request
title: slack_bolt.adapter.wsgi.http_request
---

## WsgiHttpRequest Objects

```python
class WsgiHttpRequest()
```

Extracts request information from the WSGI web server using the PEP 3333 standard.

PEP 3333: https://peps.python.org/pep-3333/

#### \_\_init\_\_

```python
def __init__(environ: WSGIEnvironment)
```

#### method: `str`

#### path: `str`

#### query\_string: `str`

#### protocol: `str`

#### get\_headers

```python
def get_headers() -> Dict[str, Union[str, Sequence[str]]]
```

#### get\_body

```python
def get_body() -> str
```
