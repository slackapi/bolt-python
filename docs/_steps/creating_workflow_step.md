---
title: Creating workflow steps
lang: en
slug: creating-steps
order: 2
---

<div class='section-content'>

To create a workflow step, Bolt provides the `WorkflowStep` class.

When instantiating a new `WorkflowStep`, pass in the step's `callback_id` and a configuration object.

The configuration object contains three keys: `edit`, `save`, and `execute`. Each of these keys must be a single callback or a list of callbacks. All callbacks have access to a `step` object that contains information about the workflow step event.

After instantiating a `WorkflowStep`, you can pass it into `app.step()`. Behind the scenes, your app will listen and respond to the workflow step’s events using the callbacks provided in the configuration object.

</div>

```python
from slack_bolt import App, WorkflowStep

# Initiate the Bolt app as you normally would
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Create a new WorkflowStep instance
ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)

# Pass Step to set up listeners
app.step(ws)
```
