---
sidebar_label: utils
title: slack_bolt.kwargs_injection.utils
---

## BoltRequest Objects

```python
class BoltRequest()
```

#### raw\_body

#### query

#### headers

#### content\_type

#### body

#### context

#### lazy\_only

#### lazy\_function\_name

#### mode

either &quot;http&quot; or &quot;socket_mode&quot;

#### \_\_init\_\_

```python
def __init__(*,
             body: Union[str, dict],
             query: Optional[Union[str, Dict[str, str],
                                   Dict[str, Sequence[str]]]] = None,
             headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None,
             context: Optional[Dict[str, Any]] = None,
             mode: str = "http")
```

Request to a Bolt app.

**Arguments**:

- `body` - The raw request body (only plain text is supported for &quot;http&quot; mode)
- `query` - The query string data in any data format.
- `headers` - The request headers.
- `context` - The context in this request.
- `mode` - The mode used for this request. (either &quot;http&quot; or &quot;socket_mode&quot;)

#### to\_copyable

```python
def to_copyable() -> "BoltRequest"
```

## BoltResponse Objects

```python
class BoltResponse()
```

#### status

#### body

#### headers

#### \_\_init\_\_

```python
def __init__(*,
             status: int,
             body: Union[str, dict] = "",
             headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None)
```

The response from a Bolt app.

**Arguments**:

- `status` - HTTP status code
- `body` - The response body (dict and str are supported)
- `headers` - The response headers.

#### first\_headers

```python
def first_headers() -> Dict[str, str]
```

#### first\_headers\_without\_set\_cookie

```python
def first_headers_without_set_cookie() -> Dict[str, str]
```

#### cookies

```python
def cookies() -> Sequence[SimpleCookie]
```

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

#### client

`slack_sdk.web.WebClient` instance with a valid token

#### logger

Logger instance

#### req

Incoming request from Slack

#### resp

Response representation

#### request

Incoming request from Slack

#### response

Response representation

#### context

Context data associated with the incoming request

#### body

Parsed request body data

#### payload

The unwrapped core data in the request body

#### options

An alias for payload in an `@app.options` listener

#### shortcut

An alias for payload in an `@app.shortcut` listener

#### action

An alias for payload in an `@app.action` listener

#### view

An alias for payload in an `@app.view` listener

#### command

An alias for payload in an `@app.command` listener

#### event

An alias for payload in an `@app.event` listener

#### message

An alias for payload in an `@app.message` listener

#### ack

`ack()` utility function, which returns acknowledgement to the Slack servers

#### say

`say()` utility function, which calls `chat.postMessage` API with the associated channel ID

#### respond

`respond()` utility function, which utilizes the associated `response_url`

#### complete

`complete()` utility function, signals a successful completion of the custom function

#### fail

`fail()` utility function, signal that the custom function failed to complete

#### set\_status

`set_status()` utility function for AI Agents &amp; Assistants

#### set\_title

`set_title()` utility function for AI Agents &amp; Assistants

#### set\_suggested\_prompts

`set_suggested_prompts()` utility function for AI Agents &amp; Assistants

#### get\_thread\_context

`get_thread_context()` utility function for AI Agents &amp; Assistants

#### save\_thread\_context

`save_thread_context()` utility function for AI Agents &amp; Assistants

#### say\_stream

`say_stream()` utility function for conversations, AI Agents &amp; Assistants

#### next

`next()` utility function, which tells the middleware chain that it can continue with the next one

#### next\_

An alias of `next()` for avoiding the Python built-in method overrides in middleware functions

#### \_\_init\_\_

```python
def __init__(*,
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

#### to\_options

```python
def to_options(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### to\_shortcut

```python
def to_shortcut(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### to\_action

```python
def to_action(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### to\_view

```python
def to_view(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### to\_command

```python
def to_command(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### to\_event

```python
def to_event(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### to\_message

```python
def to_message(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### to\_step

```python
def to_step(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### warning\_skip\_uncommon\_arg\_name

```python
def warning_skip_uncommon_arg_name(arg_name: str) -> str
```

#### build\_required\_kwargs

```python
def build_required_kwargs(*,
                          logger: logging.Logger,
                          required_arg_names: MutableSequence[str],
                          request: BoltRequest,
                          response: Optional[BoltResponse],
                          next_func: Optional[Callable[[], None]] = None,
                          this_func: Optional[Callable] = None,
                          error: Optional[Exception] = None,
                          next_keys_required: bool = True) -> Dict[str, Any]
```

