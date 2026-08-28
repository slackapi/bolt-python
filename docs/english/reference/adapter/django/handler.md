---
sidebar_label: handler
title: slack_bolt.adapter.django.handler
---

#### to\_bolt\_request

```python
def to_bolt_request(req: HttpRequest) -> BoltRequest
```

#### to\_django\_response

```python
def to_django_response(bolt_resp: BoltResponse) -> HttpResponse
```

#### release\_thread\_local\_connections

```python
def release_thread_local_connections(logger: Logger, execution_timing: str)
```

## DjangoListenerStartHandler Objects

```python
class DjangoListenerStartHandler(ListenerStartHandler)
```

Django sets DB connections as a thread-local variable per thread.

If the thread is not managed on the Django app side, the connections won't be released by Django.
This handler releases the connections every time a ThreadListenerRunner execution completes.

#### handle

```python
def handle(request: BoltRequest, response: Optional[BoltResponse]) -> None
```

## DjangoListenerCompletionHandler Objects

```python
class DjangoListenerCompletionHandler(ListenerCompletionHandler)
```

Django sets DB connections as a thread-local variable per thread.

If the thread is not managed on the Django app side, the connections won't be released by Django.
This handler releases the connections every time a ThreadListenerRunner execution completes.

#### handle

```python
def handle(request: BoltRequest, response: Optional[BoltResponse]) -> None
```

## DjangoThreadLazyListenerRunner Objects

```python
class DjangoThreadLazyListenerRunner(ThreadLazyListenerRunner)
```

#### start

```python
def start(function: Callable[..., None], request: BoltRequest) -> None
```

## SlackRequestHandler Objects

```python
class SlackRequestHandler()
```

#### \_\_init\_\_

```python
def __init__(app: App)
```

#### handle

```python
def handle(req: HttpRequest) -> HttpResponse
```
