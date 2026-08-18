---
sidebar_label: get_thread_context
title: slack_bolt.context.get_thread_context
---

## Submodules

- [slack_bolt.context.get_thread_context.async_get_thread_context](/tools/bolt-python/reference/context/get_thread_context/async_get_thread_context)
- [slack_bolt.context.get_thread_context.get_thread_context](/tools/bolt-python/reference/context/get_thread_context/get_thread_context)

## GetThreadContext Objects

```python
class GetThreadContext()
```

#### thread\_context\_store: `AssistantThreadContextStore`

#### payload: `dict`

#### channel\_id: `str`

#### thread\_ts: `str`

#### thread\_context\_loaded: `bool`

#### \_\_init\_\_

```python
def __init__(thread_context_store: AssistantThreadContextStore,
             channel_id: str, thread_ts: str, payload: dict)
```

