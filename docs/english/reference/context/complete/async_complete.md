---
sidebar_label: async_complete
title: slack_bolt.context.complete.async_complete
---

## AsyncComplete Objects

```python
class AsyncComplete()
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

Check if this complete function has been called.

**Returns**:

- `bool` - True if the complete function has been called, False otherwise.
