---
sidebar_label: async_callback_options
title: slack_bolt.oauth.async_callback_options
---

## CallbackResponseBuilder Objects

```python
class CallbackResponseBuilder()
```

## AsyncBoltRequest Objects

```python
class AsyncBoltRequest()
```

#### raw\_body

#### body

#### query

#### headers

#### content\_type

#### context

#### lazy\_only

#### lazy\_function\_name

#### mode

either &quot;http&quot; or &quot;socket_mode&quot;

#### to\_copyable

```python
def to_copyable() -> "AsyncBoltRequest"
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

## AsyncSuccessArgs Objects

```python
class AsyncSuccessArgs()
```

## AsyncFailureArgs Objects

```python
class AsyncFailureArgs()
```

## AsyncCallbackOptions Objects

```python
class AsyncCallbackOptions()
```

#### success

#### failure

## DefaultAsyncCallbackOptions Objects

```python
class DefaultAsyncCallbackOptions(AsyncCallbackOptions)
```

#### success

#### failure

