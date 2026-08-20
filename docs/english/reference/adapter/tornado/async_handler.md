---
sidebar_label: async_handler
title: slack_bolt.adapter.tornado.async_handler
---

## AsyncSlackEventsHandler Objects

```python
class AsyncSlackEventsHandler(RequestHandler)
```

#### initialize

```python
def initialize(app: AsyncApp)
```

#### post

```python
async def post()
```

## AsyncSlackOAuthHandler Objects

```python
class AsyncSlackOAuthHandler(RequestHandler)
```

#### initialize

```python
def initialize(app: AsyncApp)
```

#### get

```python
async def get()
```

#### to\_async\_bolt\_request

```python
def to_async_bolt_request(req: HTTPServerRequest) -> AsyncBoltRequest
```
