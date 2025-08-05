# ホームタブの更新

[ホームタブ](/surfaces/app-home)は、サイドバーや検索画面からアクセス可能なサーフェスエリアです。アプリはこのエリアを使ってユーザーごとのビューを表示することができます。アプリ設定ページで App Home の機能を有効にすると、[`views.publish`](/reference/methods/views.publish) API メソッドの呼び出しで `user_id` と[ビューのペイロード](/reference/interaction-payloads/view-interactions-payload/#view_submission)を指定して、ホームタブを公開・更新することができるようになります。

[`app_home_opened`](/reference/events/app_home_opened) イベントをサブスクライブすると、ユーザーが App Home を開く操作をリッスンできます。

指定可能な引数の一覧は [モジュールドキュメント](https://docs.slack.dev/bolt-python/reference/kwargs_injection/args.html)を参考にしてください。

```python
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        # 組み込みのクライアントを使って views.publish を呼び出す
        client.views_publish(
            # イベントに関連づけられたユーザー ID を使用
            user_id=event["user"],
            # アプリの設定で予めホームタブが有効になっている必要がある
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome home, <@" + event["user"] + "> :house:*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                          "type": "mrkdwn",
                          "text":"Learn how home tabs can be more useful and interactive </surfaces/app-home|*in the documentation*>."
                        }
                    }
                ]
            }
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
```