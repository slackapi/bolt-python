---
sidebar_label: complete
title: slack_bolt.workflows.step.utilities.complete
---

## Complete Objects

```python
class Complete()
```

`complete()` utility to tell Slack the completion of a step from app execution.

    def execute(step, complete, fail):
        inputs = step["inputs"]
        # if everything was successful
        outputs = &#123;
            "task_name": inputs["task_name"]["value"],
            "task_description": inputs["task_description"]["value"],
        }
        complete(outputs=outputs)

    ws = WorkflowStep(
        callback_id="add_task",
        edit=edit,
        save=save,
        execute=execute,
    )
    app.step(ws)

This utility is a thin wrapper of workflows.stepCompleted API method.
Refer to https://api.slack.com/methods/workflows.stepCompleted for details.

#### \_\_init\_\_

```python
def __init__(*, client: WebClient, body: dict)
```
