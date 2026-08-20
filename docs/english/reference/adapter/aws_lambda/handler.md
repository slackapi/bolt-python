---
sidebar_label: handler
title: slack_bolt.adapter.aws_lambda.handler
---

## SlackRequestHandler Objects

```python
class SlackRequestHandler()
```

#### \_\_init\_\_

```python
def __init__(app: App)
```

#### clear\_all\_log\_handlers

```python
def clear_all_log_handlers()
```

#### handle

```python
def handle(event, context)
```

#### to\_bolt\_request

```python
def to_bolt_request(event) -> BoltRequest
```

#### to\_aws\_response

```python
def to_aws_response(resp: BoltResponse) -> Dict[str, Any]
```

#### not\_found

```python
def not_found() -> Dict[str, Any]
```
