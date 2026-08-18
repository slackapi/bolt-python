---
sidebar_label: async_say
title: slack_bolt.context.say.async_say
---

#### create\_copy

```python
def create_copy(original: Any) -> Any
```

## AsyncSay Objects

```python
class AsyncSay()
```

#### client: `Optional[AsyncWebClient]`

#### channel: `Optional[str]`

#### thread\_ts: `Optional[str]`

#### build\_metadata: `Optional[Callable[[], Awaitable[Union[Dict, Metadata]]]]`

#### \_\_init\_\_

```python
def __init__(
    client: Optional[AsyncWebClient],
    channel: Optional[str],
    thread_ts: Optional[str] = None,
    build_metadata: Optional[Callable[[], Awaitable[Union[Dict,
                                                          Metadata]]]] = None)
```

