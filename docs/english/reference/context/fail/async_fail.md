---
sidebar_label: async_fail
title: slack_bolt.context.fail.async_fail
---

## AsyncFail Objects

```python
class AsyncFail()
```

#### client: `AsyncWebClient`

#### function\_execution\_id: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(client: AsyncWebClient, function_execution_id: Optional[str])
```

#### has\_been\_called

```python
def has_been_called() -> bool
```

Check if this fail function has been called.

**Returns**:

- `bool` - True if the fail function has been called, False otherwise.

