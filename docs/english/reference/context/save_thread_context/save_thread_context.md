---
sidebar_label: save_thread_context
title: slack_bolt.context.save_thread_context.save_thread_context
slug: save_thread_context
---

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

## SaveThreadContext Objects

```python
class SaveThreadContext()
```

#### thread\_context\_store: `AssistantThreadContextStore`

#### channel\_id: `str`

#### thread\_ts: `str`

#### \_\_init\_\_

```python
def __init__(thread_context_store: AssistantThreadContextStore,
             channel_id: str, thread_ts: str)
```

