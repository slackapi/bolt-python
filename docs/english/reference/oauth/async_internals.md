---
sidebar_label: async_internals
title: slack_bolt.oauth.async_internals
---

#### warning\_installation\_store\_conflicts

```python
def warning_installation_store_conflicts() -> str
```

#### default\_installation\_stores: `Dict[str, AsyncInstallationStore]`

#### get\_or\_create\_default\_installation\_store

```python
def get_or_create_default_installation_store(
        client_id: str) -> AsyncInstallationStore
```

#### select\_consistent\_installation\_store

```python
def select_consistent_installation_store(
        client_id: str, app_store: Optional[AsyncInstallationStore],
        oauth_flow_store: Optional[AsyncInstallationStore],
        logger: Logger) -> Optional[AsyncInstallationStore]
```

