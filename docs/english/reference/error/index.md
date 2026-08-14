---
sidebar_label: slack_bolt.error
title: slack_bolt.error
---

Bolt specific error types.

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app

## BoltUnhandledRequestError Objects

```python
class BoltUnhandledRequestError(BoltError)
```

#### request

type: ignore[name-defined]

#### body

#### current\_response

type: ignore[name-defined]

#### last\_global\_middleware\_name

#### \_\_init\_\_

```python
def __init__(*,
             request: Union["BoltRequest", "AsyncBoltRequest"],
             current_response: Optional["BoltResponse"],
             last_global_middleware_name: Optional[str] = None)
```

