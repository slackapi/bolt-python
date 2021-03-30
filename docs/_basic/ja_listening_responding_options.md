---
title: オプションのリスニングと応答
lang: ja-jp
slug: options
order: 14
---

<div class="section-content">
`options()` メソッドは、Slack からのオプション（セレクトメニュー内の動的な選択肢）をリクエストするペイロードをリッスンします。 [`action()` と同様に](#action-listening)、文字列型の `action_id` または制約付きオブジェクトが必要です。

外部データソースを使って選択メニューをロードするためには、末部に `/slack/events` が付加された URL を Options Load URL として予め設定しておく必要があります。

`external_select` メニューでは `action_id` を指定することをおすすめしています。ただし、ダイアログを利用している場合、ダイアログが Block Kit に対応していないため、`callback_id` をフィルタリングするための制約オブジェクトを使用する必要があります。

オプションのリクエストに応答するときは、有効なオプションを含む `options` または `option_groups` のリストとともに `ack()` を呼び出す必要があります。API サイトにある[外部データを使用する選択メニューに応答するサンプル例](https://api.slack.com/reference/messaging/block-elements#external-select)と、[ダイアログでの応答例](https://api.slack.com/dialogs#dynamic_select_elements_external)を参考にしてください。

</div>

```python
# 外部データを使用する選択メニューオプションに応答するサンプル例
@app.options("external_action")
def show_options(ack):
    options = [
        {
            "text": {"type": "plain_text", "text":"Option 1"},
            "value":"1-1",
        },
        {
            "text": {"type": "plain_text", "text":"Option 2"},
            "value":"1-2",
        },
    ]
    ack(options=options)
```
