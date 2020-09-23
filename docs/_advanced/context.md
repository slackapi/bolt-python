---
title: Using context
lang: en
slug: context
order: 7
---

<div class="section-content">
All listeners have access to a `context` dictionary, which can be used to enrich events with additional information. Bolt automatically attaches information if it’s included in the incoming event, like `user_id`, `team_id`, `channel_id`, and `enterprise_id`.

`context` is just a dictionary, so you can add to it by directly modifying it.
</div>