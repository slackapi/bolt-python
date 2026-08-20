---
sidebar_label: async_utils
title: slack_bolt.kwargs_injection.async_utils
---

#### build\_async\_required\_kwargs

```python
def build_async_required_kwargs(
    *,
    logger: logging.Logger,
    required_arg_names: MutableSequence[str],
    request: AsyncBoltRequest,
    response: Optional[BoltResponse],
    next_func: Optional[Callable[[], None]] = None,
    this_func: Optional[Callable] = None,
    error: Optional[Exception] = None,
    next_keys_required: bool = True) -> Dict[str, Any]
```
