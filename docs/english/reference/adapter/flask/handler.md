---
sidebar_label: handler
title: slack_bolt.adapter.flask.handler
---

#### to\_bolt\_request

```python
def to_bolt_request(req: Request) -> BoltRequest
```

#### to\_flask\_response

```python
def to_flask_response(bolt_resp: BoltResponse) -> Response
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
def handle(req: Request) -> Response
```
