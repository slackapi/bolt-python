---
title: リスナーミドルウェア
lang: ja-jp
slug: /concepts/listener-middleware
---

リスナーミドルウェアは、それを渡したリスナーでのみ実行されるミドルウェアです。リスナーには、`middleware` パラメーターを使ってミドルウェア関数をいくつでも渡すことができます。このパラメーターには、1 つまたは複数のミドルウェア関数からなるリストを指定します。

非常にシンプルなリスナーミドルウェアの場合であれば、`next()` メソッドを呼び出す代わりに `bool` 値（処理を継続したい場合は `True`）を返すだけで済む「リスナーマッチャー」を使うとよいでしょう。

<span>指定可能な引数の一覧は<a href="https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html">モジュールドキュメント</a>を参考にしてください。</span>

```python
# ボットからのメッセージをフィルタリングするリスナーミドルウェア
def no_bot_messages(message, next):
    if "bot_id" not in message:
        next()

# このリスナーは人間によって送信されたメッセージのみを受け取ります
@app.event(event="message", middleware=[no_bot_messages])
def log_message(logger, event):
    logger.info(f"(MSG) User: {event['user']}\nMessage: {event['text']}")

# リスナーマッチャー： 簡略化されたバージョンのリスナーミドルウェア
def no_bot_messages(message) -> bool:
    return "bot_id" not in message

@app.event(
    event="message",
    matchers=[no_bot_messages]
    # or matchers=[lambda message: message.get("subtype") != "bot_message"]
)
def log_message(logger, event):
    logger.info(f"(MSG) User: {event['user']}\nMessage: {event['text']}")
```
