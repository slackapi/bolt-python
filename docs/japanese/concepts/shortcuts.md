---
title: ショートカットのリスニングと応答
lang: ja-jp
slug: /bolt-python/concepts/shortcuts
---

`shortcut()` メソッドは、[グローバルショートカット](/interactivity/implementing-shortcuts#global)と[メッセージショートカット](/interactivity/implementing-shortcuts#messages)の 2 つをサポートしています。

ショートカットは、いつでも呼び出せるアプリのエントリーポイントを提供するものです。グローバルショートカットは Slack のテキスト入力エリアや検索ウィンドウからアクセスできます。メッセージショートカットはメッセージのコンテキストメニューからアクセスできます。アプリは、ショートカットリクエストをリッスンするために `shortcut()` メソッドを使用します。このメソッドには `str` 型または `re.Pattern` 型の `callback_id` パラメーターを指定します。

ショートカットリクエストがアプリによって確認されたことを Slack に伝えるため、`ack()` を呼び出す必要があります。

ショートカットのペイロードには `trigger_id` が含まれます。アプリはこれを使って、ユーザーにやろうとしていることを確認するための[モーダルを開く](/bolt-python/concepts/opening-modals)ことができます。

アプリの設定でショートカットを登録する際は、他の URL と同じように、リクエスト URL の末尾に `/slack/events` をつけます。

⚠️ グローバルショートカットのペイロードにはチャンネル ID が **含まれません**。アプリでチャンネル ID を取得する必要がある場合は、モーダル内に [`conversations_select`](/reference/block-kit/block-elements/multi-select-menu-element#conversation_multi_select) エレメントを配置します。メッセージショートカットにはチャンネル ID が含まれます。

<span>指定可能な引数の一覧は<a href="https://docs.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html">モジュールドキュメント</a>を参考にしてください。</span>
```python
# 'open_modal' という callback_id のショートカットをリッスン
@app.shortcut("open_modal")
def open_modal(ack, shortcut, client):
    # ショートカットのリクエストを確認
    ack()
    # 組み込みのクライアントを使って views_open メソッドを呼び出す
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        # モーダルで表示するシンプルなビューのペイロード
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text":"My App"},
            "close": {"type": "plain_text", "text":"Close"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text":"About the simplest modal you could conceive of :smile:\n\nMaybe </block-kit/#making-things-interactive|*make the modal interactive*> or </surfaces/modals|*learn more advanced modal use cases*>."
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text":"Psssst this modal was designed using <https://api.slack.com/tools/block-kit-builder|*Block Kit Builder*>"
                        }
                    ]
                }
            ]
        }
    )
```

## 制約付きオブジェクトを使用したショートカットのリスニング

制約付きオブジェクトを使って `callback_id` や `type` によるリッスンできます。オブジェクト内の制約は `str` 型または `re.Pattern` オブジェクトを使用できます。

```python
# このリスナーが呼び出されるのは、callback_id が 'open_modal' と一致し
# かつ type が 'message_action' と一致するときのみ
@app.shortcut({"callback_id": "open_modal", "type": "message_action"})
def open_modal(ack, shortcut, client):
    # ショートカットのリクエストを確認
    ack()
    # 組み込みのクライアントを使って views_open メソッドを呼び出す
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text":"My App"},
            "close": {"type": "plain_text", "text":"Close"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text":"About the simplest modal you could conceive of :smile:\n\nMaybe </block-kit/#making-things-interactive|*make the modal interactive*> or </surfaces/modals|*learn more advanced modal use cases*>."
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text":"Psssst this modal was designed using <https://api.slack.com/tools/block-kit-builder|*Block Kit Builder*>"
                        }
                    ]
                }
            ]
        }
    )
```