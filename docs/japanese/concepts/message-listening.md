---
title: メッセージのリスニング
lang: ja-jp
slug: /concepts/message-listening
---

[あなたのアプリがアクセス権限を持つ](/messaging/retrieving-messages)メッセージの投稿イベントをリッスンするには `message()` メソッドを利用します。このメソッドは `type` が `message` ではないイベントを処理対象から除外します。

`message()` の引数には `str` 型または `re.Pattern` オブジェクトを指定できます。この条件のパターンに一致しないメッセージは除外されます。

<span>指定可能な引数の一覧は<a href="https://docs.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html">モジュールドキュメント</a>を参考にしてください。</span>
```python
# '👋' が含まれるすべてのメッセージに一致
@app.message(":wave:")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")
```

## 正規表現パターンの利用

文字列の代わりに `re.compile()` メソッドを使用すれば、より細やかな条件指定ができます。

```python
import re

@app.message(re.compile("(hi|hello|hey)"))
def say_hello_regex(say, context):
    # 正規表現のマッチ結果は context.matches に設定される
    greeting = context['matches'][0]
    say(f"{greeting}, how are you?")
```