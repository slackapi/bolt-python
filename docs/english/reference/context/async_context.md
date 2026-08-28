---
sidebar_label: async_context
title: slack_bolt.context.async_context
---

## `AsyncBoltContext`

Bases: BaseContext

Context object associated with a request from Slack.

### `ack`

```python
ack: AsyncAck
```

`ack()` function for this request.

```python
@app.action("button")
async def handle_button_clicks(context):
    await context.ack()

# You can access "ack" this way too.
@app.action("button")
async def handle_button_clicks(ack):
    await ack()
```

**Returns:**

- AsyncAck – Callable `ack()` function

### `actor_enterprise_id`

```python
actor_enterprise_id: Optional[str]
```

The action's actor's Enterprise Grid organization ID.

Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.

### `actor_team_id`

```python
actor_team_id: Optional[str]
```

The action's actor's workspace ID.

Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.

### `actor_user_id`

```python
actor_user_id: Optional[str]
```

The action's actor's user ID.

Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.

### `authorize_result`

```python
authorize_result: Optional[AuthorizeResult]
```

The authorize result resolved for this request.

### `bot_id`

```python
bot_id: Optional[str]
```

The bot ID resolved for this request.

### `bot_token`

```python
bot_token: Optional[str]
```

The bot token resolved for this request.

### `bot_user_id`

```python
bot_user_id: Optional[str]
```

The bot user ID resolved for this request.

### `channel_id`

```python
channel_id: Optional[str]
```

The conversation ID associated with this request.

### `client`

```python
client: AsyncWebClient
```

The `AsyncWebClient` instance available for this request.

```python
@app.event("app_mention")
async def handle_events(context):
    await context.client.chat_postMessage(
        channel=context.channel_id,
        text="Thanks!",
    )

# You can access "client" this way too.
@app.event("app_mention")
async def handle_events(client, context):
    await client.chat_postMessage(
        channel=context.channel_id,
        text="Thanks!",
    )
```

**Returns:**

- AsyncWebClient – `AsyncWebClient` instance

### `complete`

```python
complete: AsyncComplete
```

`complete()` function for this request.

Once a custom function's state is set to complete,
any outputs the function returns will be passed along to the next step of its housing workflow,
or complete the workflow if the function is the last step in a workflow. Additionally,
any interactivity handlers associated to a function invocation will no longer be invocable.

```python
@app.function("reverse")
async def handle_button_clicks(ack, complete):
    await ack()
    await complete(outputs={"stringReverse":"olleh"})

@app.function("reverse")
async def handle_button_clicks(context):
    await context.ack()
    await context.complete(outputs={"stringReverse":"olleh"})
```

**Returns:**

- AsyncComplete – Callable `complete()` function

### `enterprise_id`

```python
enterprise_id: Optional[str]
```

The Enterprise Grid Organization ID of this request.

### `fail`

```python
fail: AsyncFail
```

`fail()` function for this request.

Once a custom function's state is set to error,
its housing workflow will be interrupted and any provided error message will be passed
on to the end user through SlackBot. Additionally, any interactivity handlers associated
to a function invocation will no longer be invocable.

```python
@app.function("reverse")
async def handle_button_clicks(ack, fail):
    await ack()
    await fail(error="something went wrong")

@app.function("reverse")
async def handle_button_clicks(context):
    await context.ack()
    await context.fail(error="something went wrong")
```

**Returns:**

- AsyncFail – Callable `fail()` function

### `function_bot_access_token`

```python
function_bot_access_token: Optional[str]
```

The bot token resolved for this function request.

Only available for `function_executed` and interactivity events scoped to a custom step.

### `function_execution_id`

```python
function_execution_id: Optional[str]
```

The `function_execution_id` associated with this request.

Only available for `function_executed` and interactivity events scoped to a custom step.

### `inputs`

```python
inputs: Optional[Dict[str, Any]]
```

The `inputs` associated with this request.

Only available for `function_executed` and interactivity events scoped to a custom step.

### `is_enterprise_install`

```python
is_enterprise_install: Optional[bool]
```

True if the request is associated with an Org-wide installation.

### `listener_runner`

```python
listener_runner: AsyncioListenerRunner
```

The properly configured listener_runner that is available for middleware/listeners.

### `logger`

```python
logger: Logger
```

The properly configured logger that is available for middleware/listeners.

### `matches`

```python
matches: Optional[Tuple]
```

Returns all the matched parts in message listener's regexp.

### `respond`

```python
respond: Optional[AsyncRespond]
```

`respond()` function for this request.

```python
@app.action("button")
async def handle_button_clicks(context):
    await context.ack()
    await context.respond("Hi!")

# You can access "ack" this way too.
@app.action("button")
async def handle_button_clicks(ack, respond):
    await ack()
    await respond("Hi!")
```

**Returns:**

- Optional[AsyncRespond] – Callable `respond()` function

### `response_url`

```python
response_url: Optional[str]
```

The `response_url` associated with this request.

### `say`

```python
say: AsyncSay
```

`say()` function for this request.

```python
@app.action("button")
async def handle_button_clicks(context):
    await context.ack()
    await context.say("Hi!")

# You can access "ack" this way too.
@app.action("button")
async def handle_button_clicks(ack, say):
    await ack()
    await say("Hi!")
```

**Returns:**

- AsyncSay – Callable `say()` function

### `team_id`

```python
team_id: Optional[str]
```

The Workspace ID of this request.

### `thread_ts`

```python
thread_ts: Optional[str]
```

The conversation thread's ID associated with this request.

### `token`

```python
token: Optional[str]
```

The (bot/user) token resolved for this request.

### `user_id`

```python
user_id: Optional[str]
```

The user ID associated ith this request.

### `user_token`

```python
user_token: Optional[str]
```

The user token resolved for this request.
