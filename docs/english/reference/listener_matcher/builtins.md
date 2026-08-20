---
sidebar_label: builtins
title: slack_bolt.listener_matcher.builtins
---

## BuiltinListenerMatcher Objects

```python
class BuiltinListenerMatcher(ListenerMatcher)
```

#### \_\_init\_\_

```python
def __init__(
    *,
    func: Callable[..., Union[bool, Awaitable[bool]]],
    base_logger: Optional[Logger] = None)
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
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### event

```python
def event(
    constraints: Union[str, Pattern, Dict[str, Optional[Union[str, Sequence[Optional[Union[str, Pattern]]]]]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### message\_event

```python
def message_event(
    constraints: Dict[str, Optional[Union[str, Sequence[Optional[Union[str, Pattern]]]]]],
    keyword: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### function\_executed

```python
def function_executed(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### workflow\_step\_execute

```python
def workflow_step_execute(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### command

```python
def command(
    command: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### shortcut

```python
def shortcut(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### global\_shortcut

```python
def global_shortcut(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### message\_shortcut

```python
def message_shortcut(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### action

```python
def action(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### block\_action

```python
def block_action(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### attachment\_action

```python
def attachment_action(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### dialog\_submission

```python
def dialog_submission(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### dialog\_cancellation

```python
def dialog_cancellation(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### workflow\_step\_edit

```python
def workflow_step_edit(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### view

```python
def view(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### view\_submission

```python
def view_submission(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### view\_closed

```python
def view_closed(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### workflow\_step\_save

```python
def workflow_step_save(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### options

```python
def options(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### block\_suggestion

```python
def block_suggestion(
    action_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```

#### dialog\_suggestion

```python
def dialog_suggestion(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None) -> Union[ListenerMatcher, AsyncListenerMatcher]
```
