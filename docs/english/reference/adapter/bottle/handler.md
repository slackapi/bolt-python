---
sidebar_label: handler
title: slack_bolt.adapter.bottle.handler
---

#### to\_bolt\_request

```python
def to_bolt_request(req: Request) -> BoltRequest
```

#### set\_response

```python
def set_response(bolt_resp: BoltResponse, resp: Response) -> None
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
def handle(req: Request, resp: Response) -> str
```
