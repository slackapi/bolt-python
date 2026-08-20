---
sidebar_label: payload_utils
title: slack_bolt.request.payload_utils
---

#### to\_event

```python
def to_event(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### to\_message

```python
def to_message(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### is\_function

```python
def is_function(body: Dict[str, Any]) -> bool
```

#### is\_event

```python
def is_event(body: Dict[str, Any]) -> bool
```

#### is\_workflow\_step\_execute

```python
def is_workflow_step_execute(body: Dict[str, Any]) -> bool
```

#### is\_message\_event

```python
def is_message_event(body: Dict[str, Any]) -> bool
```

#### is\_any\_im\_message\_event

```python
def is_any_im_message_event(body: Dict[str, Any]) -> bool
```

#### is\_im\_message\_event

```python
def is_im_message_event(body: Dict[str, Any]) -> bool
```

#### is\_assistant\_event

```python
def is_assistant_event(body: Dict[str, Any]) -> bool
```

#### is\_assistant\_thread\_started\_event

```python
def is_assistant_thread_started_event(body: Dict[str, Any]) -> bool
```

#### is\_assistant\_thread\_context\_changed\_event

```python
def is_assistant_thread_context_changed_event(body: Dict[str, Any]) -> bool
```

#### is\_app\_home\_opened\_event

```python
def is_app_home_opened_event(body: Dict[str, Any], tab: Optional[str] = None) -> bool
```

#### is\_user\_message\_event\_in\_assistant\_thread

```python
def is_user_message_event_in_assistant_thread(body: Dict[str, Any]) -> bool
```

#### is\_bot\_message\_event\_in\_assistant\_thread

```python
def is_bot_message_event_in_assistant_thread(body: Dict[str, Any]) -> bool
```

#### is\_other\_message\_sub\_event\_in\_assistant\_thread

```python
def is_other_message_sub_event_in_assistant_thread(body: Dict[str, Any]) -> bool
```

#### to\_command

```python
def to_command(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### is\_slash\_command

```python
def is_slash_command(body: Dict[str, Any]) -> bool
```

#### to\_action

```python
def to_action(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### is\_action

```python
def is_action(body: Dict[str, Any]) -> bool
```

#### is\_attachment\_action

```python
def is_attachment_action(body: Dict[str, Any]) -> bool
```

#### is\_block\_actions

```python
def is_block_actions(body: Dict[str, Any]) -> bool
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

#### to\_options

```python
def to_options(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### is\_options

```python
def is_options(body: Dict[str, Any]) -> bool
```

#### is\_block\_suggestion

```python
def is_block_suggestion(body: Dict[str, Any]) -> bool
```

#### is\_dialog\_suggestion

```python
def is_dialog_suggestion(body: Dict[str, Any]) -> bool
```

#### to\_shortcut

```python
def to_shortcut(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### is\_shortcut

```python
def is_shortcut(body: Dict[str, Any]) -> bool
```

#### is\_global\_shortcut

```python
def is_global_shortcut(body: Dict[str, Any]) -> bool
```

#### is\_message\_shortcut

```python
def is_message_shortcut(body: Dict[str, Any]) -> bool
```

#### to\_view

```python
def to_view(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### is\_view

```python
def is_view(body: Dict[str, Any]) -> bool
```

#### is\_view\_submission

```python
def is_view_submission(body: Dict[str, Any]) -> bool
```

#### is\_view\_closed

```python
def is_view_closed(body: Dict[str, Any]) -> bool
```

#### is\_workflow\_step\_save

```python
def is_workflow_step_save(body: Dict[str, Any]) -> bool
```

#### to\_step

```python
def to_step(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```
