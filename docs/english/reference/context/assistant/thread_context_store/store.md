---
sidebar_label: store
title: slack_bolt.context.assistant.thread_context_store.store
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
def find(*, channel_id: str, thread_ts: str) -> Optional[AssistantThreadContext]
```
