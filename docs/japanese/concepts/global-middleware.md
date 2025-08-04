---
title: グローバルミドルウェア
lang: ja-jp
slug: /bolt-python/concepts/global-middleware
order: 8
---

グローバルミドルウェアは、すべての受信リクエストに対して、リスナーミドルウェアが呼ばれる前に実行されるものです。ミドルウェア関数を `app.use()` に渡すことで、アプリにはグローバルミドルウェアをいくつでも追加できます。ミドルウェア関数で受け取れる引数はリスナー関数と同じものに加えて`next()` 関数があります。

グローバルミドルウェアでもリスナーミドルウェアでも、次のミドルウェアに実行チェーンの制御をリレーするために、`next()` を呼び出す必要があります。 

<span>指定可能な引数の一覧は<a href="https://docs.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html">モジュールドキュメント</a>を参考にしてください。</span>

```python
@app.use
def auth_abc(client, context, logger, payload, next):
    slack_user_id = payload["user"]
    help_channel_id = "C12345"

    try:
        # Slack のユーザー ID を使って外部のシステムでユーザーを検索します
        user = abc.lookup_by_id(slack_user_id)
        # 結果を context に保存します
        context["user"] = user
    except Exception:
        client.chat_postEphemeral(
            channel=payload["channel"],
            user=slack_user_id,
            text=f"Sorry <@{slack_user_id}>, you aren't registered in ABC or there was an error with authentication.Please post in <#{help_channel_id}> for assistance"
        )

    # 次のミドルウェアに実行権を渡します
    next()
```