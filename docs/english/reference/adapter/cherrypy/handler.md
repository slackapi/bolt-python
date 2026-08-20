---
sidebar_label: handler
title: slack_bolt.adapter.cherrypy.handler
---

#### build\_bolt\_request

```python
def build_bolt_request() -> BoltRequest
```

#### set\_response\_status\_and\_headers

```python
def set_response_status_and_headers(bolt_resp: BoltResponse) -> None
```

#### slack\_in

```python
def slack_in()
```

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
def handle() -> bytes
```
