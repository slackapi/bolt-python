---
sidebar_label: say
title: slack_bolt.context.say
---

## Submodules

- [slack_bolt.context.say.async_say](/tools/bolt-python/reference/context/say/async_say)
- [slack_bolt.context.say.internals](/tools/bolt-python/reference/context/say/internals)
- [slack_bolt.context.say.say](/tools/bolt-python/reference/context/say/say)

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
    build_metadata: Optional[Callable[[], Optional[Union[Dict, Metadata]]]] = None)
```
