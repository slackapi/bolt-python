---
sidebar_label: wsgi
title: slack_bolt.adapter.wsgi
---

## `SlackRequestHandler`

```python
SlackRequestHandler(app, path='/slack/events')
```

Setup Bolt as a WSGI web framework, this will make your application compatible with WSGI web servers.

This can be used for production deployments.

With the default settings, `http://localhost:3000/slack/events`
Run Bolt with [gunicorn](https://gunicorn.org/)

```python
app = App()

api = SlackRequestHandler(app)
```

```bash
export SLACK_SIGNING_SECRET=***

export SLACK_BOT_TOKEN=xoxb-***

gunicorn app:api -b 0.0.0.0:3000 --log-level debug
```

**Parameters:**

- **app** (App) – Your bolt application
- **path** (str) – The path to handle request from Slack (Default: `/slack/events`)

## Submodules

- [slack_bolt.adapter.wsgi.handler](/tools/bolt-python/reference/adapter/wsgi/handler)
- [slack_bolt.adapter.wsgi.http_request](/tools/bolt-python/reference/adapter/wsgi/http_request)
- [slack_bolt.adapter.wsgi.http_response](/tools/bolt-python/reference/adapter/wsgi/http_response)
- [slack_bolt.adapter.wsgi.internals](/tools/bolt-python/reference/adapter/wsgi/internals)
