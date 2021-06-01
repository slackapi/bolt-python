---
title: リスナーミドルウェア
lang: ja-jp
slug: listener-middleware
order: 5
---

<div class="section-content">
リスナーミドルウェアは、それを渡したリスナーでのみ実行されるミドルウェアです。リスナーには、`middleware` パラメーターを使ってミドルウェア関数をいくつでも渡すことができます。このパラメーターには、1 つまたは複数のミドルウェア関数からなるリストを指定します。
</div>

<div>
<span class="annotation">指定可能な引数の一覧は<a href="https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html" target="_blank">モジュールドキュメント</a>を参考にしてください。</span>
```python
# "bot_message" サブタイプのメッセージを抽出するリスナーミドルウェア
def no_bot_messages(message, next):
    subtype = message.get("subtype")
    if subtype != "bot_message":
       next()

# このリスナーは人間によって送信されたメッセージのみを受け取ります
@app.event(event="message", middleware=[no_bot_messages])
def log_message(logger, event):
    logger.info(f"(MSG) User: {event['user']}
Message: {event['text']}")
```
</div>