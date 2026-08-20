---
sidebar_label: default_async_store
title: slack_bolt.context.assistant.thread_context_store.default_async_store
---

## DefaultAsyncAssistantThreadContextStore Objects

```python
class DefaultAsyncAssistantThreadContextStore(AsyncAssistantThreadContextStore)
```

#### client: `AsyncWebClient`

#### context: `AsyncBoltContext`

#### \_\_init\_\_

```python
def __init__(context: AsyncBoltContext)
```

#### save

```python
async def save(*, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None
```

#### find

```python
async def find(*, channel_id: str, thread_ts: str) -> Optional[AssistantThreadContext]
```
