---
title: アクション
lang: ja-jp
slug: /ja-jp/bolt-python/concepts/actions
---

## アクションのリスニング

Bolt アプリは `action` メソッドを用いて、ボタンのクリック、メニューの選択、メッセージショートカットなどのユーザーのアクションをリッスンすることができます。

アクションは `str` 型または `re.Pattern` 型の `action_id` でフィルタリングできます。`action_id` は、Slack プラットフォーム上のインタラクティブコンポーネントを区別する一意の識別子として機能します。

`action()` を使ったすべての例で `ack()` が使用されていることに注目してください。アクションのリスナー内では、Slack からのリクエストを受信したことを確認するために、`ack()` 関数を呼び出す必要があります。これについては、[リクエストの確認](/bolt-python/concepts/acknowledge)セクションで説明しています。

<span>指定可能な引数の一覧は<a href="https://docs.slack.dev/bolt-python/reference/kwargs_injection/args.html">モジュールドキュメント</a>を参考にしてください。</span>
```python
# 'approve_button' という action_id のブロックエレメントがトリガーされるたびに、このリスナーが呼び出させれる
@app.action("approve_button")
def update_message(ack):
    ack()
    # アクションへの反応としてメッセージを更新
```

### 制約付きオブジェクトを使用したアクションのリスニング

制約付きのオブジェクトを使用すると、`block_id` と `action_id` をそれぞれ、または任意に組み合わせてリッスンできます。オブジェクト内の制約は、`str` 型または `re.Pattern` 型で指定できます。

```python
# この関数は、block_id が 'assign_ticket' に一致し
# かつ action_id が 'select_user' に一致する場合にのみ呼び出される
@app.action({
    "block_id": "assign_ticket",
    "action_id": "select_user"
})
def update_message(ack, body, client):
    ack()

    if "container" in body and "message_ts" in body["container"]:
        client.reactions_add(
            name="white_check_mark",
            channel=body["channel"]["id"],
            timestamp=body["container"]["message_ts"],
        )
```

## アクションへの応答

アクションへの応答には、主に 2 つの方法があります。1 つ目の最も一般的なやり方は `say()` を使用する方法です。そのリクエストが発生した会話（チャンネルや DM）にメッセージを返します。

2 つ目は、`respond()` を使用する方法です。これは、アクションに関連づけられた `response_url` を使ったメッセージ送信を行うためのユーティリティです。

<span>指定可能な引数の一覧は<a href="https://docs.slack.dev/bolt-python/reference/kwargs_injection/args.html">モジュールドキュメント</a>を参考にしてください。</span>
```python
# 'approve_button' という action_id のインタラクティブコンポーネントがトリガーされると、このリスナーが呼ばれる
@app.action("approve_button")
def approve_request(ack, say):
    # アクションのリクエストを確認
    ack()
    say("Request approved 👍")
```

### respond() の利用

`respond()` は `response_url` を使って送信するときに便利なメソッドで、これらと同じような動作をします。投稿するメッセージのペイロードには、全ての[メッセージペイロードのプロパティ](/messaging/#payloads)とオプションのプロパティとして `response_type`（値は `"in_channel"` または `"ephemeral"`）、`replace_original`、`delete_original`、`unfurl_links`、`unfurl_media` などを指定できます。こうすることによってアプリから送信されるメッセージは、やり取りの発生元に反映されます。

```python
# 'user_select' という action_id を持つアクションのトリガーをリッスン
@app.action("user_select")
def select_user(ack, action, respond):
    ack()
    respond(f"You selected <@{action['selected_user']}>")
```
