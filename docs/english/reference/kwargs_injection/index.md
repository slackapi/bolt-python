---
sidebar_label: kwargs_injection
title: slack_bolt.kwargs_injection
---

For middleware/listener arguments, Bolt does flexible data injection in accordance with their names.

To learn the available arguments, check `slack_bolt.kwargs_injection.args`'s API document.
For steps from apps, checking `slack_bolt.workflows.step.utilities` as well should be helpful.

## Submodules

- [slack_bolt.kwargs_injection.args](/tools/bolt-python/reference/kwargs_injection/args)
- [slack_bolt.kwargs_injection.async_args](/tools/bolt-python/reference/kwargs_injection/async_args)
- [slack_bolt.kwargs_injection.async_utils](/tools/bolt-python/reference/kwargs_injection/async_utils)
- [slack_bolt.kwargs_injection.utils](/tools/bolt-python/reference/kwargs_injection/utils)

## Args Objects

```python
class Args()
```

All the arguments in this class are available in any middleware / listeners.
You can inject the named variables in the argument list in arbitrary order.

```python
@app.action("link_button")
def handle_buttons(ack, respond, logger, context, body, client):
    logger.info(f"request body: {body}")
    ack()
    if context.channel_id is not None:
        respond("Hi!")
    client.views_open(
        trigger_id=body["trigger_id"],
        view={ ... }
    )
```

Alternatively, you can include a parameter named `args` and it will be injected with an instance of this class.

```python
@app.action("link_button")
def handle_buttons(args):
    args.logger.info(f"request body: {args.body}")
    args.ack()
    if args.context.channel_id is not None:
        args.respond("Hi!")
    args.client.views_open(
        trigger_id=args.body["trigger_id"],
        view={ ... }
    )
```


#### client: `WebClient`

`slack_sdk.web.WebClient` instance with a valid token

#### logger: `logging.Logger`

Logger instance

#### req: `BoltRequest`

Incoming request from Slack

#### resp: `BoltResponse`

Response representation

#### request: `BoltRequest`

Incoming request from Slack

#### response: `BoltResponse`

Response representation

#### context: `BoltContext`

Context data associated with the incoming request

#### body: `Dict[str, Any]`

Parsed request body data

#### payload: `Dict[str, Any]`

The unwrapped core data in the request body

#### options: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.options` listener

#### shortcut: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.shortcut` listener

#### action: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.action` listener

#### view: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.view` listener

#### command: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.command` listener

#### event: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.event` listener

#### message: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.message` listener

#### ack: `Ack`

`ack()` utility function, which returns acknowledgement to the Slack servers

#### say: `Say`

`say()` utility function, which calls `chat.postMessage` API with the associated channel ID

#### respond: `Respond`

`respond()` utility function, which utilizes the associated `response_url`

#### complete: `Complete`

`complete()` utility function, signals a successful completion of the custom function

#### fail: `Fail`

`fail()` utility function, signal that the custom function failed to complete

#### set\_status: `Optional[SetStatus]`

`set_status()` utility function for AI Agents & Assistants

#### set\_title: `Optional[SetTitle]`

`set_title()` utility function for AI Agents & Assistants

#### set\_suggested\_prompts: `Optional[SetSuggestedPrompts]`

`set_suggested_prompts()` utility function for AI Agents & Assistants

#### get\_thread\_context: `Optional[GetThreadContext]`

`get_thread_context()` utility function for AI Agents & Assistants

#### save\_thread\_context: `Optional[SaveThreadContext]`

`save_thread_context()` utility function for AI Agents & Assistants

#### say\_stream: `Optional[SayStream]`

`say_stream()` utility function for conversations, AI Agents & Assistants

#### next: `Callable[[], None]`

`next()` utility function, which tells the middleware chain that it can continue with the next one

#### next\_: `Callable[[], None]`

An alias of `next()` for avoiding the Python built-in method overrides in middleware functions

#### \_\_init\_\_

```python
def __init__(
    *,
    logger: logging.Logger,
    client: WebClient,
    req: BoltRequest,
    resp: BoltResponse,
    context: BoltContext,
    body: Dict[str, Any],
    payload: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None,
    shortcut: Optional[Dict[str, Any]] = None,
    action: Optional[Dict[str, Any]] = None,
    view: Optional[Dict[str, Any]] = None,
    command: Optional[Dict[str, Any]] = None,
    event: Optional[Dict[str, Any]] = None,
    message: Optional[Dict[str, Any]] = None,
    ack: Ack,
    say: Say,
    respond: Respond,
    complete: Complete,
    fail: Fail,
    set_status: Optional[SetStatus] = None,
    set_title: Optional[SetTitle] = None,
    set_suggested_prompts: Optional[SetSuggestedPrompts] = None,
    get_thread_context: Optional[GetThreadContext] = None,
    save_thread_context: Optional[SaveThreadContext] = None,
    say_stream: Optional[SayStream] = None,
    next: Callable[[], None],
    **kwargs)
```

#### build\_required\_kwargs

```python
def build_required_kwargs(
    *,
    logger: logging.Logger,
    required_arg_names: MutableSequence[str],
    request: BoltRequest,
    response: Optional[BoltResponse],
    next_func: Optional[Callable[[], None]] = None,
    this_func: Optional[Callable] = None,
    error: Optional[Exception] = None,
    next_keys_required: bool = True) -> Dict[str, Any]
```
