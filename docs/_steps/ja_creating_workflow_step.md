---
title: ステップの定義
lang: ja-jp
slug: creating-steps
order: 2
---

<div class='section-content'>

ワークフローステップの作成には、Bolt が提供する `WorkflowStep` クラスを利用します。

ステップの `callback_id` と設定オブジェクトを指定して、`WorkflowStep` の新しいインスタンスを作成します。

設定オブジェクトは、`edit`、`save`、`execute` という 3 つのキーを持ちます。それぞれのキーは、単一のコールバック、またはコールバックのリストである必要があります。すべてのコールバックは、ワークフローステップのイベントに関する情報を保持する `step` オブジェクトにアクセスできます。

`WorkflowStep` のインスタンスを作成したら、それを`app.step()` メソッドに渡します。これによって、アプリがワークフローステップのイベントをリッスンし、設定オブジェクトで指定されたコールバックを使ってそれに応答できるようになります。

</div>

```python
import os
from slack_bolt import App
from slack_bolt.workflows.step import WorkflowStep

# いつも通りBolt アプリを起動する
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

def edit(ack, step, configure):
    pass

def save(ack, view, update):
    pass

def execute(step, complete, fail):
    pass

# WorkflowStep の新しいインスタンスを作成する
ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)
# ワークフローステップを渡してリスナーを設定する
app.step(ws)
```
