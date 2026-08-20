---
sidebar_label: file
title: slack_bolt.context.assistant.thread_context_store.file
---

## FileAssistantThreadContextStore Objects

```python
class FileAssistantThreadContextStore(AssistantThreadContextStore)
```

#### \_\_init\_\_

```python
def __init__(base_dir: str = str(Path.home()) + '/.bolt-app-assistant-thread-contexts')
```

#### save

```python
def save(*, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None
```

#### find

```python
def find(*, channel_id: str, thread_ts: str) -> Optional[AssistantThreadContext]
```
