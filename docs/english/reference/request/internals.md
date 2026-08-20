---
sidebar_label: internals
title: slack_bolt.request.internals
---

#### parse\_query

```python
def parse_query(
    query: Optional[Union[str, Dict[str, str], Dict[str, Sequence[str]]]]) -> Dict[str, Sequence[str]]
```

#### parse\_body

```python
def parse_body(body: str, content_type: Optional[str]) -> Dict[str, Any]
```

#### extract\_is\_enterprise\_install

```python
def extract_is_enterprise_install(payload: Dict[str, Any]) -> Optional[bool]
```

#### extract\_enterprise\_id

```python
def extract_enterprise_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_actor\_enterprise\_id

```python
def extract_actor_enterprise_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_team\_id

```python
def extract_team_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_actor\_team\_id

```python
def extract_actor_team_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_user\_id

```python
def extract_user_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_actor\_user\_id

```python
def extract_actor_user_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_channel\_id

```python
def extract_channel_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_thread\_ts

```python
def extract_thread_ts(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_function\_execution\_id

```python
def extract_function_execution_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_function\_bot\_access\_token

```python
def extract_function_bot_access_token(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_function\_inputs

```python
def extract_function_inputs(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### build\_context

```python
def build_context(context: BoltContext, body: Dict[str, Any]) -> BoltContext
```

#### extract\_content\_type

```python
def extract_content_type(headers: Dict[str, Sequence[str]]) -> Optional[str]
```

#### build\_normalized\_headers

```python
def build_normalized_headers(
    headers: Optional[Dict[str, Union[str, Sequence[str]]]]) -> Dict[str, Sequence[str]]
```

#### error\_message\_raw\_body\_required\_in\_http\_mode

```python
def error_message_raw_body_required_in_http_mode() -> str
```

#### debug\_multiple\_response\_urls\_detected

```python
def debug_multiple_response_urls_detected() -> str
```
