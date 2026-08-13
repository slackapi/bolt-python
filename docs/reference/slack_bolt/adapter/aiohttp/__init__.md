---
sidebar_label: aiohttp
title: slack_bolt.adapter.aiohttp
---

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

#### to\_bolt\_request

```python
async def to_bolt_request(request: web.Request) -> AsyncBoltRequest
```

#### to\_aiohttp\_response

```python
async def to_aiohttp_response(bolt_resp: BoltResponse) -> web.Response
```

