---
sidebar_label: async_complete
title: slack_bolt.workflows.step.utilities.async_complete
---

## AsyncComplete Objects

```python
class AsyncComplete()
```

`complete()` utility to tell Slack the completion of a step from app execution.

```python
    async def execute(step, complete, fail):
        inputs = step["inputs"]
        # if everything was successful
        outputs = {
            "task_name": inputs["task_name"]["value"],
            "task_description": inputs["task_description"]["value"],
        }
        await complete(outputs=outputs)

    ws = AsyncWorkflowStep(
        callback_id="add_task",
        edit=edit,
        save=save,
        execute=execute,
    )
    app.step(ws)
```

This utility is a thin wrapper of workflows.stepCompleted API method.
Refer to https://api.slack.com/methods/workflows.stepCompleted for details.

#### \_\_init\_\_

```python
def __init__(*, client: AsyncWebClient, body: dict)
```
