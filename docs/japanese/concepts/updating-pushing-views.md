# モーダルの更新と多重表示

モーダル内では、複数のモーダルをスタックのように重ねることができます。[`views_open`](/reference/methods/views.open/) という APIを呼び出すと、親となるとなるモーダルビューが追加されます。この最初の呼び出しの後、[`views_update`](/reference/methods/views.update/) を呼び出すことでそのビューを更新することができます。また、[`views_push`](/reference/methods/views.push) を呼び出すと、親のモーダルの上にさらに新しいモーダルビューを重ねることもできます。

**`views_update`**

モーダルの更新は、組み込みのクライアントで `views_update` API を呼び出します。この API呼び出しでは、ビューを開いた時に生成された `view_id` と、更新後の `blocks` のリストを含む新しい `view` を指定します。既存のモーダルに含まれるエレメントをユーザーが操作した時にビューを更新する場合は、リクエストの `body` に含まれる `view_id` が利用できます。

**`views_push`**

既存のモーダルの上に新しいモーダルをスタックのように追加する場合は、組み込みのクライアントで `views_push` API を呼び出します。この API 呼び出しでは、有効な `trigger_id` と新しい[ビューのペイロード](/reference/interaction-payloads/view-interactions-payload/#view_submission)を指定します。`views_push` の引数は [モーダルの開始](#creating-modals) と同じです。モーダルを開いた後、このモーダルのスタックに追加できるモーダルビューは 2 つまでです。

モーダルの更新と多重表示に関する詳細は、[API ドキュメント](/surfaces/modals)を参照してください。

指定可能な引数の一覧は[モジュールドキュメント](https://docs.slack.dev/tools/bolt-python/reference/kwargs_injection/args.html)を参考にしてください。

```python
# モーダルに含まれる、`button_abc` という action_id のボタンの呼び出しをリッスン
@app.action("button_abc")
def update_modal(ack, body, client):
    # ボタンのリクエストを確認
    ack()
    # 組み込みのクライアントで views_update を呼び出し
    client.views_update(
        # view_id を渡すこと
        view_id=body["view"]["id"],
        # 競合状態を防ぐためのビューの状態を示す文字列
        hash=body["view"]["hash"],
        # 更新後の blocks を含むビューのペイロード
        view={
            "type": "modal",
            # ビューの識別子
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text":"Updated modal"},
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "plain_text", "text":"You updated the modal!"}
                },
                {
                    "type": "image",
                    "image_url": "https://media.giphy.com/media/SVZGEcYt7brkFUyU90/giphy.gif",
                    "alt_text":"Yay!The modal was updated"
                }
            ]
        }
    )
```