---
sidebar_label: aws_lambda
title: slack_bolt.adapter.aws_lambda
---

## Submodules

- [slack_bolt.adapter.aws_lambda.chalice_handler](/tools/bolt-python/reference/adapter/aws_lambda/chalice_handler)
- [slack_bolt.adapter.aws_lambda.chalice_lazy_listener_runner](/tools/bolt-python/reference/adapter/aws_lambda/chalice_lazy_listener_runner)
- [slack_bolt.adapter.aws_lambda.handler](/tools/bolt-python/reference/adapter/aws_lambda/handler)
- [slack_bolt.adapter.aws_lambda.internals](/tools/bolt-python/reference/adapter/aws_lambda/internals)
- [slack_bolt.adapter.aws_lambda.lambda_s3_oauth_flow](/tools/bolt-python/reference/adapter/aws_lambda/lambda_s3_oauth_flow)
- [slack_bolt.adapter.aws_lambda.lazy_listener_runner](/tools/bolt-python/reference/adapter/aws_lambda/lazy_listener_runner)
- [slack_bolt.adapter.aws_lambda.local_lambda_client](/tools/bolt-python/reference/adapter/aws_lambda/local_lambda_client)

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
