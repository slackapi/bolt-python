---
sidebar_label: fail
title: slack_bolt.workflows.step.utilities.fail
---

## `Fail`

```python
Fail(*, client, body)
```

`fail()` utility to tell Slack the execution failure of a step from app.

```python
def execute(step, complete, fail):
    inputs = step["inputs"]
    # if something went wrong
    error = {"message": "Just testing step failure!"}
    fail(error=error)


ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)
app.step(ws)
```

This utility is a thin wrapper of workflows.stepFailed API method.
Refer to https://api.slack.com/methods/workflows.stepFailed for details.
