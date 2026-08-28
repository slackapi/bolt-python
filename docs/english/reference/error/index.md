---
sidebar_label: error
title: slack_bolt.error
---

Bolt specific error types.

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app.

## BoltUnhandledRequestError Objects

```python
class BoltUnhandledRequestError(BoltError)
```

#### request: `BoltRequest`

#### body: `dict`

#### current\_response: `Optional[BoltResponse]`

#### last\_global\_middleware\_name: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(
    *,
    request: Union[BoltRequest, AsyncBoltRequest],
    current_response: Optional[BoltResponse],
    last_global_middleware_name: Optional[str] = None)
```
