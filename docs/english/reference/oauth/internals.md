---
sidebar_label: internals
title: slack_bolt.oauth.internals
---

## CallbackResponseBuilder Objects

```python
class CallbackResponseBuilder()
```

#### \_\_init\_\_

```python
def __init__(
    *,
    logger: Logger,
    state_utils: OAuthStateUtils,
    redirect_uri_page_renderer: RedirectUriPageRenderer)
```

#### default\_installation\_stores: `Dict[str, InstallationStore]`

#### get\_or\_create\_default\_installation\_store

```python
def get_or_create_default_installation_store(client_id: str) -> InstallationStore
```

#### select\_consistent\_installation\_store

```python
def select_consistent_installation_store(
    client_id: str,
    app_store: Optional[InstallationStore],
    oauth_flow_store: Optional[InstallationStore],
    logger: Logger) -> Optional[InstallationStore]
```

#### build\_detailed\_error

```python
def build_detailed_error(reason: str) -> str
```
