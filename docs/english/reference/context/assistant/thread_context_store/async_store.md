---
sidebar_label: async_store
title: slack_bolt.context.assistant.thread_context_store.async_store
---

## AssistantThreadContext Objects

```python
class AssistantThreadContext(dict)
```

#### enterprise\_id: `Optional[str]`

#### team\_id: `Optional[str]`

#### channel\_id: `str`

#### \_\_init\_\_

```python
def __init__(payload: dict)
```

## AsyncAssistantThreadContextStore Objects

```python
class AsyncAssistantThreadContextStore()
```

#### save

```python
async def save(*, channel_id: str, thread_ts: str, context: Dict[str,
                                                                 str]) -> None
```

#### find

```python
async def find(*, channel_id: str,
               thread_ts: str) -> Optional[AssistantThreadContext]
```

