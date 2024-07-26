---
title: Creating workflow steps
lang: en
slug: /concepts/creating-steps
---

:::danger

Workflow Steps from Apps are a deprecated feature.

Workflow Steps from Apps are different than, and not interchangable with, Slack automation workflows. We encourage those who are currently publishing Workflow Steps from Apps to consider the new [Slack automation features](https://api.slack.com/automation), such as custom functions for Bolt.

Please [read the Slack API changelog entry](https://api.slack.com/changelog/2023-08-workflow-steps-from-apps-step-back) for more information.

:::

To create a workflow step, Bolt provides the `WorkflowStep` class.

When instantiating a new `WorkflowStep`, pass in the step's `callback_id` and a configuration object.

The configuration object contains three keys: `edit`, `save`, and `execute`. Each of these keys must be a single callback or a list of callbacks. All callbacks have access to a `step` object that contains information about the workflow step event.

After instantiating a `WorkflowStep`, you can pass it into `app.step()`. Behind the scenes, your app will listen and respond to the workflow step’s events using the callbacks provided in the configuration object.

Alternatively, workflow steps can also be created using the `WorkflowStepBuilder` class alongside a decorator pattern. For more information, including an example of this approach, [refer to the documentation](https://slack.dev/bolt-python/api-docs/slack_bolt/workflows/step/step.html#slack_bolt.workflows.step.step.WorkflowStepBuilder).




Refer to the module documents (<a href="https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html">common</a> / <a href="https://slack.dev/bolt-python/api-docs/slack_bolt/workflows/step/utilities/index.html">step-specific</a>) to learn the available arguments.

```python
import os
from slack_bolt import App
from slack_bolt.workflows.step import WorkflowStep

# Initiate the Bolt app as you normally would
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

def edit(ack, step, configure):
    pass

def save(ack, view, update):
    pass

def execute(step, complete, fail):
    pass

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


