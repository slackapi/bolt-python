---
sidebar_label: complete
title: slack_bolt.context.complete
---

## Complete Objects

```python
class Complete()
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

Check if this complete function has been called.

**Returns**:

- `bool` - True if the complete function has been called, False otherwise.

