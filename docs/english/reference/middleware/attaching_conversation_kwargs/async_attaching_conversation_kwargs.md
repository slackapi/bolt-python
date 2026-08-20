---
sidebar_label: async_attaching_conversation_kwargs
title: slack_bolt.middleware.attaching_conversation_kwargs.async_attaching_conversation_kwargs
---

## AsyncAttachingConversationKwargs Objects

```python
class AsyncAttachingConversationKwargs(AsyncMiddleware)
```

#### thread\_context\_store: `Optional[AsyncAssistantThreadContextStore]`

#### \_\_init\_\_

```python
def __init__(thread_context_store: Optional[AsyncAssistantThreadContextStore] = None)
```

#### async\_process

```python
async def async_process(
    *,
    req: AsyncBoltRequest,
    resp: BoltResponse,
    next: Callable[[], Awaitable[BoltResponse]]) -> Optional[BoltResponse]
```
