---
sidebar_label: internals
title: slack_bolt.oauth.internals
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

#### warning\_installation\_store\_conflicts

```python
def warning_installation_store_conflicts() -> str
```

## CallbackResponseBuilder Objects

```python
class CallbackResponseBuilder()
```

#### default\_installation\_stores

#### get\_or\_create\_default\_installation\_store

```python
def get_or_create_default_installation_store(
        client_id: str) -> InstallationStore
```

#### select\_consistent\_installation\_store

```python
def select_consistent_installation_store(
        client_id: str, app_store: Optional[InstallationStore],
        oauth_flow_store: Optional[InstallationStore],
        logger: Logger) -> Optional[InstallationStore]
```

#### build\_detailed\_error

```python
def build_detailed_error(reason: str) -> str
```

