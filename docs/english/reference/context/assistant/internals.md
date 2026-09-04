---
sidebar_label: internals
title: slack_bolt.context.assistant.internals
---

## `has_channel_id_and_thread_ts`

```python
has_channel_id_and_thread_ts(payload)
```

Verifies if the given payload has both channel_id and thread_ts under assistant_thread property.

This data pattern is available for assistant_* events.
