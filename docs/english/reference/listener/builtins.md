---
sidebar_label: builtins
title: slack_bolt.listener.builtins
---

## TokenRevocationListeners Objects

```python
class TokenRevocationListeners()
```

Listener functions to handle token revocation / uninstallation events.

#### installation\_store: `InstallationStore`

#### \_\_init\_\_

```python
def __init__(installation_store: InstallationStore)
```

#### handle\_tokens\_revoked\_events

```python
def handle_tokens_revoked_events(event: dict, context: BoltContext) -> None
```

#### handle\_app\_uninstalled\_events

```python
def handle_app_uninstalled_events(context: BoltContext) -> None
```
