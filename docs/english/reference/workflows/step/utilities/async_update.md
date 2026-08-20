---
sidebar_label: async_update
title: slack_bolt.workflows.step.utilities.async_update
---

## AsyncUpdate Objects

```python
class AsyncUpdate()
```

`update()` utility to tell Slack the processing results of a `save` listener.

    async def save(ack, view, update):
        await ack()

        values = view["state"]["values"]
        task_name = values["task_name_input"]["name"]
        task_description = values["task_description_input"]["description"]

        inputs = &#123;
            "task_name": &#123;"value": task_name["value"]},
            "task_description": &#123;"value": task_description["value"]}
        }
        outputs = [
            &#123;
                "type": "text",
                "name": "task_name",
                "label": "Task name",
            },
            &#123;
                "type": "text",
                "name": "task_description",
                "label": "Task description",
            }
        ]
        await update(inputs=inputs, outputs=outputs)

    ws = AsyncWorkflowStep(
        callback_id="add_task",
        edit=edit,
        save=save,
        execute=execute,
    )
    app.step(ws)

This utility is a thin wrapper of workflows.stepFailed API method.
Refer to https://api.slack.com/methods/workflows.updateStep for details.

#### \_\_init\_\_

```python
def __init__(*, client: AsyncWebClient, body: dict)
```
