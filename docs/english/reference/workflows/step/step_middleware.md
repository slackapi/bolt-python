---
sidebar_label: step_middleware
title: slack_bolt.workflows.step.step_middleware
---

## WorkflowStepMiddleware Objects

```python
class WorkflowStepMiddleware(Middleware)
```

Base middleware for step from app specific ones.

#### \_\_init\_\_

```python
def __init__(step: WorkflowStep)
```

#### process

```python
def process(
    *,
    req: BoltRequest,
    resp: BoltResponse,
    next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```
