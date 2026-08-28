---
sidebar_label: async_step_middleware
title: slack_bolt.workflows.step.async_step_middleware
---

## AsyncWorkflowStepMiddleware Objects

```python
class AsyncWorkflowStepMiddleware(AsyncMiddleware)
```

Base middleware for step from app specific ones.

#### \_\_init\_\_

```python
def __init__(step: AsyncWorkflowStep)
```

#### async\_process

```python
async def async_process(
    *,
    req: AsyncBoltRequest,
    resp: BoltResponse,
    next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```
