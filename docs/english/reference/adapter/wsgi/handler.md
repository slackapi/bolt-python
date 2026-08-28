---
sidebar_label: handler
title: slack_bolt.adapter.wsgi.handler
---

## SlackRequestHandler Objects

```python
class SlackRequestHandler()
```

#### \_\_init\_\_

```python
def __init__(app: App, path: str = '/slack/events')
```

Setup Bolt as a WSGI web framework, this will make your application compatible with WSGI web servers.

This can be used for production deployments.

With the default settings, `http://localhost:3000/slack/events`
Run Bolt with [gunicorn](https://gunicorn.org/)

# Python
    app = App()

```python
api = SlackRequestHandler(app)
```

# bash
    export SLACK_SIGNING_SECRET=***

```python
export SLACK_BOT_TOKEN=xoxb-***

gunicorn app:api -b 0.0.0.0:3000 --log-level debug
```


**Arguments**:

- `app` _App_ - Your bolt application
- `path` _str_ - The path to handle request from Slack (Default: `/slack/events`)

#### dispatch

```python
def dispatch(request: WsgiHttpRequest) -> BoltResponse
```

#### handle\_installation

```python
def handle_installation(request: WsgiHttpRequest) -> BoltResponse
```

#### handle\_callback

```python
def handle_callback(request: WsgiHttpRequest) -> BoltResponse
```
