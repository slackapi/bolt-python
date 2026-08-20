---
sidebar_label: custom_listener
title: slack_bolt.listener.custom_listener
---

## CustomListener Objects

```python
class CustomListener(Listener)
```

#### app\_name: `str`

#### ack\_function: `Callable[..., Optional[BoltResponse]]`

#### lazy\_functions: `Sequence[Callable[..., None]]`

#### matchers: `Sequence[ListenerMatcher]`

#### middleware: `Sequence[Middleware]`

#### auto\_acknowledgement: `bool`

#### ack\_timeout: `int`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(
    *,
    app_name: str,
    ack_function: Callable[..., Optional[BoltResponse]],
    lazy_functions: Sequence[Callable[..., None]],
    matchers: Sequence[ListenerMatcher],
    middleware: Sequence[Middleware],
    auto_acknowledgement: bool = False,
    ack_timeout: int = 3,
    base_logger: Optional[Logger] = None)
```

#### run\_ack\_function

```python
def run_ack_function(
    *,
    request: BoltRequest,
    response: BoltResponse) -> Optional[BoltResponse]
```
