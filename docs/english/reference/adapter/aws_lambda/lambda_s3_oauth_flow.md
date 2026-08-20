---
sidebar_label: lambda_s3_oauth_flow
title: slack_bolt.adapter.aws_lambda.lambda_s3_oauth_flow
---

## LambdaS3OAuthFlow Objects

```python
class LambdaS3OAuthFlow(OAuthFlow)
```

#### \_\_init\_\_

```python
def __init__(
    *,
    client: Optional[WebClient] = None,
    logger: Optional[Logger] = None,
    settings: Optional[OAuthSettings] = None,
    oauth_state_bucket_name: Optional[str] = None,
    installation_bucket_name: Optional[str] = None)
```

#### client

```python
@property
def client() -> WebClient
```

#### logger

```python
@property
def logger() -> Logger
```
