---
title: Handling errors
lang: en
slug: errors
order: 3
---

<div class="section-content">
If an error occurs in a listener, you can handle it directly using a `try`/`except` block. Errors associated with your app will be of type `BoltError`. Errors associated with calling Slack APIs will be of type `SlackApiError`.

By default, the global error handler will log all non-handled exceptions to the console. To handle global errors yourself, you can attach a global error handler to your app using the `app.error(fn)` function.
</div>

```python
@app.error
def customErrorHandler(error, request, response, logger):
    logger.exception(f"error: {error}")
```