---
sidebar_label: aiohttp
title: slack_bolt.adapter.asgi.aiohttp
---

## `AsyncSlackRequestHandler`

```python
AsyncSlackRequestHandler(app, path='/slack/events')
```

Bases: SlackRequestHandler

Setup Bolt as an ASGI web framework, this will make your application compatible with ASGI web servers.

This can be used for production deployment.

With the default settings, `http://localhost:3000/slack/events`
Run Bolt with [uvicron](https://www.uvicorn.org/)

```python
app = AsyncApp()
api = SlackRequestHandler(app)
```

```bash
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***
uvicorn app:api --port 3000 --log-level debug
```

**Parameters:**

- **app** (AsyncApp) – Your bolt application
- **path** (str) – The path to handle request from Slack (Default: `/slack/events`)
