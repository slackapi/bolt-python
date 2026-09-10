---
sidebar_label: async_server
title: slack_bolt.app.async_server
---

## `AsyncSlackAppServer`

```python
AsyncSlackAppServer(port, path, app, host=None)
```

Standalone AIOHTTP Web Server.

Refer to https://docs.aiohttp.org/en/stable/web.html for details of AIOHTTP.

**Parameters:**

- **port** (int) – The port to listen on
- **path** (str) – The path to receive incoming requests from Slack
- **app** (AsyncApp) – The `AsyncApp` instance that is used for processing requests
- **host** (Optional[str]) – The hostname to serve the web endpoints. (Default: 0.0.0.0)

### `start`

```python
start(host=None)
```

Starts a new web server process.
