---
sidebar_label: default_store
title: slack_bolt.context.assistant.thread_context_store.default_store
---

## DefaultAssistantThreadContextStore Objects

```python
class DefaultAssistantThreadContextStore(AssistantThreadContextStore)
```

#### client: `WebClient`

#### context: `BoltContext`

#### \_\_init\_\_

```python
def __init__(context: BoltContext)
```

#### save

```python
def save(*, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None
```

#### find

```python
def find(*, channel_id: str, thread_ts: str) -> Optional[AssistantThreadContext]
```
