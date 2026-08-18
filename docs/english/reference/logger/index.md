---
sidebar_label: logger
title: slack_bolt.logger
---


Bolt for Python relies on the standard `logging` module.

## Submodules

- [slack_bolt.logger.messages](/tools/bolt-python/reference/logger/messages)

#### get\_bolt\_logger

```python
def get_bolt_logger(cls: Any, base_logger: Optional[Logger] = None) -> Logger
```

#### get\_bolt\_app\_logger

```python
def get_bolt_app_logger(app_name: str,
                        cls: object = None,
                        base_logger: Optional[Logger] = None) -> Logger
```

