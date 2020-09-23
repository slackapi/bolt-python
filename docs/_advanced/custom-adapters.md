---
title: Custom adapters
lang: en
slug: custom-adapters
order: 1
---

<div class="section-content">
[Adapters](#adapters) are flexible and can be adjusted based on the framework you prefer. There are two necessary components of adapters:

- `__init__(app: App)`: Constructor that accepts and stores an instance of the Bolt `App`.
- `handle(req: Request)`: Function (typically named `handle()`) that receives incoming Slack requests, parses them to conform to an instance of [`BoltRequest`](https://github.com/slackapi/bolt-python/blob/main/slack_bolt/request/request.py#L23), then dispatches them to the stored Bolt app.

`BoltRequest` instantiation accepts four parameters:

| Parameter | Description | Required? |
|-----------|-------------|-----------|
| `body: str` | The raw request body | **Yes** |
| `query: any` | The query string data | No |
| `headers: Dict[str, Union[str, List[str]]]` | Request headers | No |
| `context: Dict[str, str]` | Any context for the request | No |

`BoltRequest` will return [an instance of `BoltResponse`](https://github.com/slackapi/bolt-python/blob/main/slack_bolt/request/request.py#L23) from the Bolt app.

For more in-depth examples of custom adapters, look at the implementations of the [built-in adapters](https://github.com/slackapi/bolt-python/tree/main/slack_bolt/adapter).
</div>