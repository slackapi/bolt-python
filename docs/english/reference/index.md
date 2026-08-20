---
sidebar_label: slack_bolt
title: slack_bolt
---

A Python framework to build Slack apps in a flash with the latest platform features. Read the [getting started guide](https://docs.slack.dev/tools/bolt-python/creating-an-app) and look at our [code examples](https://github.com/slackapi/bolt-python/tree/main/examples) to learn how to build apps using Bolt.

* Website: https://docs.slack.dev/tools/bolt-python/
* GitHub repository: https://github.com/slackapi/bolt-python
* The class representing a Bolt app: `slack_bolt.app.app`

## Submodules

- [slack_bolt.adapter](/tools/bolt-python/reference/adapter)
- [slack_bolt.app](/tools/bolt-python/reference/app)
- [slack_bolt.async_app](/tools/bolt-python/reference/async_app)
- [slack_bolt.authorization](/tools/bolt-python/reference/authorization)
- [slack_bolt.context](/tools/bolt-python/reference/context)
- [slack_bolt.error](/tools/bolt-python/reference/error)
- [slack_bolt.kwargs_injection](/tools/bolt-python/reference/kwargs_injection)
- [slack_bolt.lazy_listener](/tools/bolt-python/reference/lazy_listener)
- [slack_bolt.listener](/tools/bolt-python/reference/listener)
- [slack_bolt.listener_matcher](/tools/bolt-python/reference/listener_matcher)
- [slack_bolt.logger](/tools/bolt-python/reference/logger)
- [slack_bolt.middleware](/tools/bolt-python/reference/middleware)
- [slack_bolt.oauth](/tools/bolt-python/reference/oauth)
- [slack_bolt.request](/tools/bolt-python/reference/request)
- [slack_bolt.response](/tools/bolt-python/reference/response)
- [slack_bolt.util](/tools/bolt-python/reference/util)
- [slack_bolt.version](/tools/bolt-python/reference/version)
- [slack_bolt.workflows](/tools/bolt-python/reference/workflows)

## App Objects

```python
class App()
```

## BoltContext Objects

```python
class BoltContext(BaseContext)
```

Context object associated with a request from Slack.

## Ack Objects

```python
class Ack()
```

## Complete Objects

```python
class Complete()
```

## Fail Objects

```python
class Fail()
```

## Respond Objects

```python
class Respond()
```

## Say Objects

```python
class Say()
```

## SayStream Objects

```python
class SayStream()
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


## Listener Objects

```python
class Listener()
```

## CustomListenerMatcher Objects

```python
class CustomListenerMatcher(ListenerMatcher)
```

## BoltRequest Objects

```python
class BoltRequest()
```

## BoltResponse Objects

```python
class BoltResponse()
```

## Assistant Objects

```python
class Assistant(Middleware)
```

#### thread\_context\_store: `Optional[AssistantThreadContextStore]`

#### base\_logger: `Optional[logging.Logger]`

#### \_\_init\_\_

```python
def __init__(
    *,
    app_name: str = 'assistant',
    thread_context_store: Optional[AssistantThreadContextStore] = None,
    logger: Optional[logging.Logger] = None)
```

#### thread\_started

```python
def thread_started(
    *args,
    matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
    middleware: Optional[Union[Callable, Middleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

#### user\_message

```python
def user_message(
    *args,
    matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
    middleware: Optional[Union[Callable, Middleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

#### bot\_message

```python
def bot_message(
    *args,
    matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
    middleware: Optional[Union[Callable, Middleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

#### thread\_context\_changed

```python
def thread_context_changed(
    *args,
    matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
    middleware: Optional[Union[Callable, Middleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

#### default\_thread\_context\_changed

```python
def default_thread_context_changed(
    save_thread_context: SaveThreadContext,
    payload: dict)
```

#### process

```python
def process(
    *,
    req: BoltRequest,
    resp: BoltResponse,
    next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

#### build\_listener

```python
def build_listener(
    listener_or_functions: Union[Listener, Callable, List[Callable]],
    matchers: Optional[List[Union[ListenerMatcher, Callable[..., bool]]]] = None,
    middleware: Optional[List[Middleware]] = None,
    base_logger: Optional[Logger] = None) -> Listener
```

## AssistantThreadContext Objects

```python
class AssistantThreadContext(dict)
```

#### enterprise\_id: `Optional[str]`

#### team\_id: `Optional[str]`

#### channel\_id: `str`

#### \_\_init\_\_

```python
def __init__(payload: dict)
```

## AssistantThreadContextStore Objects

```python
class AssistantThreadContextStore()
```

#### save

```python
def save(*, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None
```

#### find

```python
def find(*, channel_id: str, thread_ts: str) -> Optional[AssistantThreadContext]
```

## FileAssistantThreadContextStore Objects

```python
class FileAssistantThreadContextStore(AssistantThreadContextStore)
```

#### \_\_init\_\_

```python
def __init__(base_dir: str = str(Path.home()) + '/.bolt-app-assistant-thread-contexts')
```

#### save

```python
def save(*, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None
```

#### find

```python
def find(*, channel_id: str, thread_ts: str) -> Optional[AssistantThreadContext]
```

## SetStatus Objects

```python
class SetStatus()
```

## SetTitle Objects

```python
class SetTitle()
```

## SetSuggestedPrompts Objects

```python
class SetSuggestedPrompts()
```

## SaveThreadContext Objects

```python
class SaveThreadContext()
```
