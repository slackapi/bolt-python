---
title: モーダルの送信のリスニング
lang: ja-jp
slug: view_submissions
order: 12
---

<div class="section-content">

<a href="https://api.slack.com/reference/block-kit/views">モーダルのペイロード</a>に input ブロックを含める場合、その入力値を受け取るために`view_submission` イベントをリッスンする必要があります。`view_submission` イベントのリッスンには、組み込みの`view()` メソッドを利用することができます。`view()` の引数には、`str` 型または `re.Pattern` 型の `callback_id` を指定します。

`input` ブロックの値にアクセスするには `state` オブジェクトを参照します。`state` 内には `values` というオブジェクトがあり、`block_id` と一意の `action_id` に紐づける形で入力値を保持しています。

モーダルの送信について詳しくは、<a href="https://api.slack.com/surfaces/modals/using#interactions">API ドキュメント</a>を参照してください。

</div>

<div>
<span class="annotation">指定可能な引数の一覧は<a href="https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html" target="_blank">モジュールドキュメント</a>を参考にしてください。</span>
```python
# view_submission イベントを処理
@app.view("view_1")
def handle_submission(ack, body, client, view, logger):
    # `block_c`という block_id に `dreamy_input` を持つ input ブロックがある場合
    hopes_and_dreams = view["state"]["values"]["block_c"]["dreamy_input"]
    user = body["user"]["id"]
    # 入力値を検証
    errors = {}
    if hopes_and_dreams is not None and len(hopes_and_dreams) <= 5:
        errors["block_c"] = "The value must be longer than 5 characters"
    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return
    # view_submission イベントの確認を行い、モーダルを閉じる
    ack()
    # 入力されたデータを使った処理を実行。このサンプルでは DB に保存する処理を行う
    # そして入力値の検証結果をユーザーに送信

    # ユーザーに送信するメッセージ
    msg = ""
    try:
        # DB に保存
        msg = f"Your submission of {hopes_and_dreams} was successful"
    except Exception as e:
        # エラーをハンドリング
        msg = "There was an error with your submission"

    # ユーザーにメッセージを送信
    try:
        client.chat_postMessage(channel=user, text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")

```
</div>