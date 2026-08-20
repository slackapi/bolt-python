---
sidebar_label: local_lambda_client
title: slack_bolt.adapter.aws_lambda.local_lambda_client
---

## LocalLambdaClient Objects

```python
class LocalLambdaClient(BaseClient)
```

Lambda client implementing `invoke` for use when running with Chalice CLI.

#### \_\_init\_\_

```python
def __init__(app: Chalice, config: Config) -> None
```

#### invoke

```python
def invoke(
    FunctionName: str,
    InvocationType: str = 'Event',
    Payload: str = '{}') -> InvokeResponse
```
