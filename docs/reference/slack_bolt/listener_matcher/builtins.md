---
sidebar_label: builtins
title: slack_bolt.listener_matcher.builtins
---

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app

#### is\_block\_actions

```python
def is_block_actions(body: Dict[str, Any]) -> bool
```

#### is\_function

```python
def is_function(body: Dict[str, Any]) -> bool
```

#### is\_global\_shortcut

```python
def is_global_shortcut(body: Dict[str, Any]) -> bool
```

#### is\_message\_shortcut

```python
def is_message_shortcut(body: Dict[str, Any]) -> bool
```

#### is\_attachment\_action

```python
def is_attachment_action(body: Dict[str, Any]) -> bool
```

#### is\_dialog\_submission

```python
def is_dialog_submission(body: Dict[str, Any]) -> bool
```

#### is\_dialog\_cancellation

```python
def is_dialog_cancellation(body: Dict[str, Any]) -> bool
```

#### is\_workflow\_step\_edit

```python
def is_workflow_step_edit(body: Dict[str, Any]) -> bool
```

#### is\_slash\_command

```python
def is_slash_command(body: Dict[str, Any]) -> bool
```

#### is\_event

```python
def is_event(body: Dict[str, Any]) -> bool
```

#### is\_view\_submission

```python
def is_view_submission(body: Dict[str, Any]) -> bool
```

#### is\_view\_closed

```python
def is_view_closed(body: Dict[str, Any]) -> bool
```

#### is\_block\_suggestion

```python
def is_block_suggestion(body: Dict[str, Any]) -> bool
```

#### is\_dialog\_suggestion

```python
def is_dialog_suggestion(body: Dict[str, Any]) -> bool
```

#### is\_shortcut

```python
def is_shortcut(body: Dict[str, Any]) -> bool
```

#### to\_action

```python
def to_action(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### is\_workflow\_step\_save

```python
def is_workflow_step_save(body: Dict[str, Any]) -> bool
```

#### error\_message\_event\_type

```python
def error_message_event_type(event_type: Union[str, Pattern]) -> str
```

#### get\_arg\_names\_of\_callable

```python
def get_arg_names_of_callable(func: Callable) -> List[str]
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

## ListenerMatcher Objects

```python
class ListenerMatcher(metaclass=ABCMeta)
```

#### matches

```python
@abstractmethod
def matches(req: BoltRequest, resp: BoltResponse) -> bool
```

Matches against the request and returns True if matched.

**Arguments**:

- `req` - The request
- `resp` - The response
  

**Returns**:

  True if matched.

#### get\_bolt\_logger

```python
def get_bolt_logger(cls: Any, base_logger: Optional[Logger] = None) -> Logger
```

## BuiltinListenerMatcher Objects

```python
class BuiltinListenerMatcher(ListenerMatcher)
```

#### matches

```python
def matches(req: BoltRequest, resp: BoltResponse) -> bool
```

#### build\_listener\_matcher

```python
def build_listener_matcher(
    func: Callable[..., bool],
    asyncio: bool,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### event

```python
def event(
    constraints: Union[
        str,
        Pattern,
        Dict[str, Optional[Union[str, Sequence[Optional[Union[str,
                                                              Pattern]]]]]],
    ],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### message\_event

```python
def message_event(
    constraints: Dict[str,
                      Optional[Union[str,
                                     Sequence[Optional[Union[str,
                                                             Pattern]]]]]],
    keyword: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### function\_executed

```python
def function_executed(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### workflow\_step\_execute

```python
def workflow_step_execute(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### command

```python
def command(
    command: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### shortcut

```python
def shortcut(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### global\_shortcut

```python
def global_shortcut(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### message\_shortcut

```python
def message_shortcut(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### action

```python
def action(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### block\_action

```python
def block_action(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### attachment\_action

```python
def attachment_action(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### dialog\_submission

```python
def dialog_submission(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### dialog\_cancellation

```python
def dialog_cancellation(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### workflow\_step\_edit

```python
def workflow_step_edit(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### view

```python
def view(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### view\_submission

```python
def view_submission(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### view\_closed

```python
def view_closed(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### workflow\_step\_save

```python
def workflow_step_save(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### options

```python
def options(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### block\_suggestion

```python
def block_suggestion(
    action_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### dialog\_suggestion

```python
def dialog_suggestion(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

