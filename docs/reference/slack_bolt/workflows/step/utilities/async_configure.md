---
sidebar_label: async_configure
title: slack_bolt.workflows.step.utilities.async_configure
---

## AsyncConfigure Objects

```python
class AsyncConfigure()
```

`configure()` utility to send the modal view in Workflow Builder.

```python
    async def edit(ack, step, configure):
        await ack()

        blocks = [
            {
                "type": "input",
                "block_id": "task_name_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "name",
                    "placeholder": {"type": "plain_text", "text": "Add a task name"},
                },
                "label": {"type": "plain_text", "text": "Task name"},
            },
        ]
        await configure(blocks=blocks)

    ws = AsyncWorkflowStep(
        callback_id="add_task",
        edit=edit,
        save=save,
        execute=execute,
    )
    app.step(ws)
```

Refer to https://docs.slack.dev/legacy/legacy-steps-from-apps/ for details.

