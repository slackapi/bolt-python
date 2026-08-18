---
sidebar_label: async_get_thread_context
title: slack_bolt.context.get_thread_context.async_get_thread_context
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

## AsyncGetThreadContext Objects

```python
class AsyncGetThreadContext()
```

#### thread\_context\_store: `AsyncAssistantThreadContextStore`

#### payload: `dict`

#### channel\_id: `str`

#### thread\_ts: `str`

#### thread\_context\_loaded: `bool`

#### \_\_init\_\_

```python
def __init__(thread_context_store: AsyncAssistantThreadContextStore,
             channel_id: str, thread_ts: str, payload: dict)
```

