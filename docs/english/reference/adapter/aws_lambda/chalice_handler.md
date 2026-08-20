---
sidebar_label: chalice_handler
title: slack_bolt.adapter.aws_lambda.chalice_handler
---

## ChaliceSlackRequestHandler Objects

```python
class ChaliceSlackRequestHandler()
```

#### \_\_init\_\_

```python
def __init__(app: App, chalice: Chalice, lambda_client: Optional[BaseClient] = None)
```

#### clear\_all\_log\_handlers

```python
def clear_all_log_handlers()
```

#### handle

```python
def handle(request: Request)
```

#### to\_bolt\_request

```python
def to_bolt_request(request: Request, body: str) -> BoltRequest
```

#### to\_chalice\_response

```python
def to_chalice_response(resp: BoltResponse) -> Response
```

#### not\_found

```python
def not_found() -> Response
```
