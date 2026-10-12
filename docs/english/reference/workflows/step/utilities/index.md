---
sidebar_label: utilities
title: slack_bolt.workflows.step.utilities
---

Utilities specific to steps from apps.

In steps from apps listeners, you can use a few specific listener/middleware arguments.

### `edit` listener

* `slack_bolt.workflows.step.utilities.configure` for building a modal view

### `save` listener

* `slack_bolt.workflows.step.utilities.update` for updating the step metadata

### `execute` listener

* `slack_bolt.workflows.step.utilities.fail` for notifying the execution failure to Slack
* `slack_bolt.workflows.step.utilities.complete` for notifying the execution completion to Slack

For asyncio-based apps, refer to the corresponding `async` prefixed ones.

## Submodules

- [slack_bolt.workflows.step.utilities.async_complete](/tools/bolt-python/reference/workflows/step/utilities/async_complete)
- [slack_bolt.workflows.step.utilities.async_configure](/tools/bolt-python/reference/workflows/step/utilities/async_configure)
- [slack_bolt.workflows.step.utilities.async_fail](/tools/bolt-python/reference/workflows/step/utilities/async_fail)
- [slack_bolt.workflows.step.utilities.async_update](/tools/bolt-python/reference/workflows/step/utilities/async_update)
- [slack_bolt.workflows.step.utilities.complete](/tools/bolt-python/reference/workflows/step/utilities/complete)
- [slack_bolt.workflows.step.utilities.configure](/tools/bolt-python/reference/workflows/step/utilities/configure)
- [slack_bolt.workflows.step.utilities.fail](/tools/bolt-python/reference/workflows/step/utilities/fail)
- [slack_bolt.workflows.step.utilities.update](/tools/bolt-python/reference/workflows/step/utilities/update)
