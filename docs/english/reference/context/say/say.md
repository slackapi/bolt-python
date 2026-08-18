---
sidebar_label: say
title: slack_bolt.context.say.say
slug: say
---

#### create\_copy

```python
def create_copy(original: Any) -> Any
```

## Say Objects

```python
class Say()
```

#### client: `Optional[WebClient]`

#### channel: `Optional[str]`

#### thread\_ts: `Optional[str]`

#### metadata: `Optional[Union[Dict, Metadata]]`

#### build\_metadata: `Optional[Callable[[], Optional[Union[Dict, Metadata]]]]`

#### \_\_init\_\_

```python
def __init__(
    client: Optional[WebClient],
    channel: Optional[str],
    thread_ts: Optional[str] = None,
    metadata: Optional[Union[Dict, Metadata]] = None,
    build_metadata: Optional[Callable[[], Optional[Union[Dict,
                                                         Metadata]]]] = None)
```

