---
sidebar_label: custom_listener_matcher
title: slack_bolt.listener_matcher.custom_listener_matcher
---

## CustomListenerMatcher Objects

```python
class CustomListenerMatcher(ListenerMatcher)
```

#### app\_name: `str`

#### func: `Callable[..., bool]`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(
    *,
    app_name: str,
    func: Callable[..., bool],
    base_logger: Optional[Logger] = None)
```

#### matches

```python
def matches(req: BoltRequest, resp: BoltResponse) -> bool
```
