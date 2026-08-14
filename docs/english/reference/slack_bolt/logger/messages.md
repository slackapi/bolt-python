---
sidebar_label: messages
title: slack_bolt.logger.messages
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

#### is\_action

```python
def is_action(body: Dict[str, Any]) -> bool
```

#### is\_event

```python
def is_event(body: Dict[str, Any]) -> bool
```

#### is\_function

```python
def is_function(body: Dict[str, Any]) -> bool
```

#### is\_options

```python
def is_options(body: Dict[str, Any]) -> bool
```

#### is\_shortcut

```python
def is_shortcut(body: Dict[str, Any]) -> bool
```

#### is\_slash\_command

```python
def is_slash_command(body: Dict[str, Any]) -> bool
```

#### is\_view\_submission

```python
def is_view_submission(body: Dict[str, Any]) -> bool
```

#### is\_view\_closed

```python
def is_view_closed(body: Dict[str, Any]) -> bool
```

#### is\_workflow\_step\_edit

```python
def is_workflow_step_edit(body: Dict[str, Any]) -> bool
```

#### is\_workflow\_step\_save

```python
def is_workflow_step_save(body: Dict[str, Any]) -> bool
```

#### is\_workflow\_step\_execute

```python
def is_workflow_step_execute(body: Dict[str, Any]) -> bool
```

#### error\_client\_invalid\_type

```python
def error_client_invalid_type() -> str
```

#### error\_client\_invalid\_type\_async

```python
def error_client_invalid_type_async() -> str
```

#### error\_oauth\_flow\_invalid\_type\_async

```python
def error_oauth_flow_invalid_type_async() -> str
```

#### error\_oauth\_settings\_invalid\_type\_async

```python
def error_oauth_settings_invalid_type_async() -> str
```

#### error\_auth\_test\_failure

```python
def error_auth_test_failure(error_response: SlackResponse) -> str
```

#### error\_token\_required

```python
def error_token_required() -> str
```

#### error\_unexpected\_listener\_middleware

```python
def error_unexpected_listener_middleware(middleware_type) -> str
```

#### error\_listener\_function\_must\_be\_coro\_func

```python
def error_listener_function_must_be_coro_func(func_name: str) -> str
```

#### error\_authorize\_conflicts

```python
def error_authorize_conflicts() -> str
```

#### error\_message\_event\_type

```python
def error_message_event_type(event_type: Union[str, Pattern]) -> str
```

#### error\_installation\_store\_required\_for\_builtin\_listeners

```python
def error_installation_store_required_for_builtin_listeners() -> str
```

#### error\_oauth\_flow\_or\_authorize\_required

```python
def error_oauth_flow_or_authorize_required() -> str
```

#### warning\_client\_prioritized\_and\_token\_skipped

```python
def warning_client_prioritized_and_token_skipped() -> str
```

#### warning\_token\_skipped

```python
def warning_token_skipped() -> str
```

#### warning\_installation\_store\_conflicts

```python
def warning_installation_store_conflicts() -> str
```

#### warning\_unhandled\_by\_global\_middleware

```python
def warning_unhandled_by_global_middleware(
        name: str, req: Union[BoltRequest, "AsyncBoltRequest"]) -> str
```

#### warning\_unhandled\_request

```python
def warning_unhandled_request(
        req: Union[BoltRequest, "AsyncBoltRequest"]) -> str
```

#### warning\_did\_not\_call\_ack

```python
def warning_did_not_call_ack(listener_name: str) -> str
```

#### warning\_bot\_only\_conflicts

```python
def warning_bot_only_conflicts() -> str
```

#### warning\_skip\_uncommon\_arg\_name

```python
def warning_skip_uncommon_arg_name(arg_name: str) -> str
```

#### warning\_ack\_timeout\_has\_no\_effect

```python
def warning_ack_timeout_has_no_effect(identifier: Union[str, Pattern],
                                      ack_timeout: int) -> str
```

#### info\_default\_oauth\_settings\_loaded

```python
def info_default_oauth_settings_loaded() -> str
```

#### debug\_applying\_middleware

```python
def debug_applying_middleware(middleware_name: str) -> str
```

#### debug\_checking\_listener

```python
def debug_checking_listener(listener_name: str) -> str
```

#### debug\_running\_listener

```python
def debug_running_listener(listener_name: str) -> str
```

#### debug\_running\_lazy\_listener

```python
def debug_running_lazy_listener(func_name: str) -> str
```

#### debug\_responding

```python
def debug_responding(status: int, body: str, millis: int) -> str
```

#### debug\_return\_listener\_middleware\_response

```python
def debug_return_listener_middleware_response(listener_name: str, status: int,
                                              body: str,
                                              starting_time: float) -> str
```

