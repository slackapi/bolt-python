---
sidebar_label: store
title: slack_bolt.context.assistant.thread_context_store.store
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

## AssistantThreadContextStore Objects

```python
class AssistantThreadContextStore()
```

#### save

```python
def save(*, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None
```

#### find

```python
def find(*, channel_id: str,
         thread_ts: str) -> Optional[AssistantThreadContext]
```

