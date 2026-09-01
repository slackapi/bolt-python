---
sidebar_label: asgi
title: slack_bolt.adapter.asgi
---

## `SlackRequestHandler`

```python
SlackRequestHandler(app, path='/slack/events')
```

Bases: BaseSlackRequestHandler

Setup Bolt as an ASGI web framework, this will make your application compatible with ASGI web servers.

This can be used for production deployment.

With the default settings, `http://localhost:3000/slack/events`
Run Bolt with [uvicron](https://www.uvicorn.org/)

```python
app = App()
api = SlackRequestHandler(app)
```

```bash
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***
uvicorn app:api --port 3000 --log-level debug
```

**Parameters:**

- **app** (App) – Your bolt application
- **path** (str) – The path to handle request from Slack (Default: `/slack/events`)

## Submodules

- [slack_bolt.adapter.asgi.aiohttp](/tools/bolt-python/reference/adapter/asgi/aiohttp)
- [slack_bolt.adapter.asgi.async_handler](/tools/bolt-python/reference/adapter/asgi/async_handler)
- [slack_bolt.adapter.asgi.base_handler](/tools/bolt-python/reference/adapter/asgi/base_handler)
- [slack_bolt.adapter.asgi.builtin](/tools/bolt-python/reference/adapter/asgi/builtin)
- [slack_bolt.adapter.asgi.http_request](/tools/bolt-python/reference/adapter/asgi/http_request)
- [slack_bolt.adapter.asgi.http_response](/tools/bolt-python/reference/adapter/asgi/http_response)
- [slack_bolt.adapter.asgi.utils](/tools/bolt-python/reference/adapter/asgi/utils)
