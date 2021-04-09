---
title: Lazy listeners (FaaS)
lang: en
slug: lazy-listeners
order: 9
---

<div class="section-content">
⚠️ Lazy listener functions are a beta feature to make it easier to deploy Bolt for Python apps to FaaS environments. As the feature is developed, Bolt for Python's API is subject to change.

Typically you'd call `ack()` as the first step of your listener functions. Calling `ack()` tells Slack that you've received the event and are handling it in within reasonable amount of time (3 seconds).

However, apps running on FaaS or similar runtimes that don't allow you to run threads or processes after returning an HTTP response cannot follow this pattern. Instead, you should set the `process_before_response` flag to `True`. This allows you to create a listener that calls `ack()` and handles the event safely, though you still need to complete everything within 3 seconds. For events, while a listener doesn't need `ack()` method call as you normally would, the listener needs to complete within 3 seconds, too.

Lazy listeners can be a solution for this issue. Rather than acting as a decorator, lazy listeners take two keyword args:
* `ack: Callable`: Responsible for calling `ack()`
* `lazy: List[Callable]`: Responsible for handling any time-consuming processes related to the event. The lazy function does not have access to `ack()`.
</div>

```python
def respond_to_slack_within_3_seconds(body, ack):
    text = body.get("text")
    if text is None or len(text) == 0:
        ack(f":x: Usage: /start-process (description here)")
    else:
        ack(f"Accepted! (task: {body['text']})")

import time
def run_long_process(respond, body):
    time.sleep(5)  # longer than 3 seconds
    respond(f"Completed! (task: {body['text']})")

app.command("/start-process")(
    # ack() is still called within 3 seconds
    ack=respond_to_slack_within_3_seconds,
    # Lazy function is responsible for processing the event
    lazy=[run_long_process]
)
```

<details class="secondary-wrapper">
<summary class="section-head" markdown="0">
<h4 class="section-head">Example with AWS Lambda</h4>
</summary>

<div class="secondary-content" markdown="0">
This example deploys the code to [AWS Lambda](https://aws.amazon.com/lambda/). There are more examples within the [`examples` folder](https://github.com/slackapi/bolt-python/tree/main/examples/aws_lambda).

```bash
pip install slack_bolt
# Save the source code as main.py
# and refer handler as `handler: main.handler` in config.yaml

# https://pypi.org/project/python-lambda/
pip install python-lambda

# Configure config.yml properly
# lambda:InvokeFunction & lambda:GetFunction are required for running lazy listeners
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***
echo 'slack_bolt' > requirements.txt
lambda deploy --config-file config.yaml --requirements requirements.txt
```
</div>

```python
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

# process_before_response must be True when running on FaaS
app = App(process_before_response=True)

def respond_to_slack_within_3_seconds(body, ack):
    text = body.get("text")
    if text is None or len(text) == 0:
        ack(":x: Usage: /start-process (description here)")
    else:
        ack(f"Accepted! (task: {body['text']})")

import time
def run_long_process(respond, body):
    time.sleep(5)  # longer than 3 seconds
    respond(f"Completed! (task: {body['text']})")

app.command("/start-process")(
    ack=respond_to_slack_within_3_seconds,  # responsible for calling `ack()`
    lazy=[run_long_process]  # unable to call `ack()` / can have multiple functions
)

def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
```

Please note that the followig IAM permissions would be required for running this example app.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction",
                "lambda:GetFunction"
            ],
            "Resource": "*"
        }
    ]
}
```
</details>
