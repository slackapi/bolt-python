---
title: Lazy listener functions (beta)
lang: en
slug: lazy-listener-functions
order: 1
---

<div class="section-content">
Lazy listener function is a **beta** feature that is available only in Bolt for Python. Your application can easily start asynchronous executions with Slack payloads. This feature is particularly useful for FaaS (Function as a Service) users.

To learn the reason why this feature matters for FaaS users, click **"Why is this feature useful for FaaS users?"**.

To deploy the code on the right side to [AWS Lambda](https://aws.amazon.com/lambda/) environment, follow the instructions below.

```bash
pip install slack_bolt
# Save the source code as main.py
# and refer handler as `handler: main.handler` in config.yaml

pip install python-lambda
# https://pypi.org/project/python-lambda/
# Configure config.yml properly (AWSLambdaFullAccess required)

export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***
echo 'slack_bolt' > requirements.txt
lambda deploy --config-file config.yaml --requirements requirements.txt
```
</div>

```python
from slack_bolt import App
# process_before_response must be True when running on FaaS
app = App(process_before_response=True)

def respond_to_slack_within_3_seconds(body, ack):
    if "text" in body:
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

from slack_bolt.adapter.aws_lambda import SlackRequestHandler
def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
```

<details class="secondary-wrapper">
<summary class="section-head" markdown="0">
<h4 class="section-head">Why is this feature useful for FaaS users?</h4>
</summary>

<div class="secondary-content" markdown="0">

For common Bolt apps, you can call `ack()` at the beginning of a listener function this way:
</div>

```python
@app.shortcut("callback-id-here")
def open_modal(ack, body, client):
    ack()  # acknowledge within 3 seconds
    run_time_consuming_operation_here()
```

<div class="secondary-content" markdown="0">
However, if you run your app on FaaS or a similar runtime (that doesn't allow running threads/processes after returning an HTTP response), you will use the `process_before_response=True` option to hold off sending an HTTP response util completing all the tasks in a listener. In this case, all your listener functions must complete within 3 seconds.
</div>

```python
app = App(process_before_response=True)

@app.command("/hello")
def this_always_times_out(ack):
    ack()  # will be held off for 5 seconds
    time.sleep(5)
```

<div class="secondary-content" markdown="0">
To deal with this, you can use keyword args `ack: Callable` and `lazy: List[Callable]`:

* `ack: Callable` is responsible for calling `ack()`
* `lazy: List[Callable]`  are unable to call `ack()` but can do any time consuming operations in a separate execution (in a thread, another AWS Lambda invocation, and so on)

Instead of acting as a decorator for a method, `App`/`AsyncApp`'s methods takes keyword args as below.
</div>

```python
app.command("/start-process")(
    # ack function is responsible for calling `ack()`
    ack=respond_to_slack_within_3_seconds,
    # lazy functions are unable to call `ack()`
    lazy=[run_long_process]
)
```

</details>
