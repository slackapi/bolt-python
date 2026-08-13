---
sidebar_label: callback_options
title: slack_bolt.oauth.callback_options
---

## CallbackResponseBuilder Objects

```python
class CallbackResponseBuilder()
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

## SuccessArgs Objects

```python
class SuccessArgs()
```

## FailureArgs Objects

```python
class FailureArgs()
```

## CallbackOptions Objects

```python
class CallbackOptions()
```

#### success

#### failure

## DefaultCallbackOptions Objects

```python
class DefaultCallbackOptions(CallbackOptions)
```

#### success

#### failure

