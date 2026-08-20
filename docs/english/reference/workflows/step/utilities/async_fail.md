---
sidebar_label: async_fail
title: slack_bolt.workflows.step.utilities.async_fail
---

## AsyncFail Objects

```python
class AsyncFail()
```

`fail()` utility to tell Slack the execution failure of a step from app.

```python
    async def execute(step, complete, fail):
        inputs = step["inputs"]
        # if something went wrong
        error = {"message": "Just testing step failure!"}
        await fail(error=error)

    ws = AsyncWorkflowStep(
        callback_id="add_task",
        edit=edit,
        save=save,
        execute=execute,
    )
    app.step(ws)
```

This utility is a thin wrapper of workflows.stepFailed API method.
Refer to https://api.slack.com/methods/workflows.stepFailed for details.

#### \_\_init\_\_

```python
def __init__(*, client: AsyncWebClient, body: dict)
```
