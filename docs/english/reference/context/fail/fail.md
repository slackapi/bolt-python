---
sidebar_label: fail
title: slack_bolt.context.fail.fail
slug: fail
---

## Fail Objects

```python
class Fail()
```

#### client

#### function\_execution\_id

#### \_\_init\_\_

```python
def __init__(client: WebClient, function_execution_id: Optional[str])
```

#### has\_been\_called

```python
def has_been_called() -> bool
```

Check if this fail function has been called.

**Returns**:

- `bool` - True if the fail function has been called, False otherwise.

