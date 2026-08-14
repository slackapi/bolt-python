---
sidebar_label: attaching_conversation_kwargs
title: slack_bolt.middleware.attaching_conversation_kwargs
---

## AttachingConversationKwargs Objects

```python
class AttachingConversationKwargs(Middleware)
```

#### thread\_context\_store

#### \_\_init\_\_

```python
def __init__(
        thread_context_store: Optional[AssistantThreadContextStore] = None)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

