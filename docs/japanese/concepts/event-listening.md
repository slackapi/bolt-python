# イベントのリスニング

`event()` メソッドを使うと、[Events API](/reference/events) の任意のイベントをリッスンできます。リッスンするイベントは、アプリの設定であらかじめサブスクライブしておく必要があります。これを利用することで、アプリがインストールされたワークスペースで何らかのイベント（例：ユーザーがメッセージにリアクションをつけた、ユーザーがチャンネルに参加した）が発生したときに、アプリに何らかのアクションを実行させることができます。

`event()` メソッドには `str` 型の `eventType` を指定する必要があります。

指定可能な引数の一覧は[モジュールドキュメント](https://docs.slack.dev/tools/bolt-python/reference/kwargs_injection/args.html)を参考にしてください。
```python
# ユーザーがワークスペースに参加した際に、自己紹介を促すメッセージを指定のチャンネルに送信
@app.event("team_join")
def ask_for_introduction(event, say):
    welcome_channel_id = "C12345"
    user_id = event["user"]
    text = f"Welcome to the team, <@{user_id}>! 🎉 You can introduce yourself in this channel."
    say(text=text, channel=welcome_channel_id)
```

## メッセージのサブタイプのフィルタリング

`message()` リスナーは `event("message")` と等価の機能を提供します。

`subtype` という追加のキーを指定して、イベントのサブタイプでフィルタリングすることもできます。よく使われるサブタイプには、`bot_message` や `message_replied` があります。詳しくは[メッセージイベントページ](/reference/events/message#subtypes)を参照してください。サブタイプなしのイベントだけにフィルターするために明に `None` を指定することもできます。

```python
# 変更されたすべてのメッセージに一致
@app.event({
    "type": "message",
    "subtype": "message_changed"
})
def log_message_change(logger, event):
    user, text = event["user"], event["text"]
    logger.info(f"The user {user} changed the message to {text}")
```