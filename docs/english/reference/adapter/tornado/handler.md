---
sidebar_label: handler
title: slack_bolt.adapter.tornado.handler
---

## SlackEventsHandler Objects

```python
class SlackEventsHandler(RequestHandler)
```

#### initialize

```python
def initialize(app: App)
```

#### post

```python
def post()
```

## SlackOAuthHandler Objects

```python
class SlackOAuthHandler(RequestHandler)
```

#### initialize

```python
def initialize(app: App)
```

#### get

```python
def get()
```

#### to\_bolt\_request

```python
def to_bolt_request(req: HTTPServerRequest) -> BoltRequest
```

#### set\_response

```python
def set_response(self, bolt_resp) -> None
```
