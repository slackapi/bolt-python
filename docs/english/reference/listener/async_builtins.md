---
sidebar_label: async_builtins
title: slack_bolt.listener.async_builtins
---

## AsyncTokenRevocationListeners Objects

```python
class AsyncTokenRevocationListeners()
```

Listener functions to handle token revocation / uninstallation events.

#### installation\_store: `AsyncInstallationStore`

#### \_\_init\_\_

```python
def __init__(installation_store: AsyncInstallationStore)
```

#### handle\_tokens\_revoked\_events

```python
async def handle_tokens_revoked_events(event: dict, context: AsyncBoltContext) -> None
```

#### handle\_app\_uninstalled\_events

```python
async def handle_app_uninstalled_events(context: AsyncBoltContext) -> None
```
