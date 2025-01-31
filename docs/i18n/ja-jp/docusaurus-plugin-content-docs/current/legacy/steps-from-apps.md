---
title: ワークフローステップの概要
lang: ja-jp
slug: /concepts/steps-from-apps
---

（アプリによる）ワークフローステップでは、処理をアプリ側で行うカスタムのワークフローステップを提供することができます。ユーザーは[ワークフロービルダー](https://api.slack.com/workflows)を使ってこれらのステップをワークフローに追加できます。

ワークフローステップは、次の 3 つのユーザーイベントで構成されます。

- ワークフローステップをワークフローに追加・変更する
- ワークフロー内のステップの設定内容を更新する
- エンドユーザーがそのステップを実行する

ワークフローステップを機能させるためには、これら 3 つのイベントすべてに対応する必要があります。

アプリを使ったワークフローステップに関する詳細は、[API ドキュメント](https://api.slack.com/workflows/steps)を参照してください。

## ステップの定義

ワークフローステップの作成には、Bolt が提供する `WorkflowStep` クラスを利用します。

ステップの `callback_id` と設定オブジェクトを指定して、`WorkflowStep` の新しいインスタンスを作成します。

設定オブジェクトは、`edit`、`save`、`execute` という 3 つのキーを持ちます。それぞれのキーは、単一のコールバック、またはコールバックのリストである必要があります。すべてのコールバックは、ワークフローステップのイベントに関する情報を保持する `step` オブジェクトにアクセスできます。

`WorkflowStep` のインスタンスを作成したら、それを`app.step()` メソッドに渡します。これによって、アプリがワークフローステップのイベントをリッスンし、設定オブジェクトで指定されたコールバックを使ってそれに応答できるようになります。

また、デコレーターとして利用できる `WorkflowStepBuilder` クラスを使ってワークフローステップを定義することもできます。 詳細は、[こちらのドキュメント](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/workflows/step/step.html#slack_bolt.workflows.step.step.WorkflowStepBuilder)のコード例などを参考にしてください。

指定可能な引数の一覧はモジュールドキュメントを参考にしてください（<a href="https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html">共通</a> / <a href="https://tools.slack.dev/bolt-python/api-docs/slack_bolt/workflows/step/utilities/index.html">ステップ用</a>

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

## ステップの追加・編集

作成したワークフローステップがワークフローに追加またはその設定を変更されるタイミングで、[`workflow_step_edit` イベントがアプリに送信されます](https://api.slack.com/reference/workflows/workflow_step_edit)。このイベントがアプリに届くと、`WorkflowStep` で設定した `edit` コールバックが実行されます。

ステップの追加と編集のどちらが行われるときも、[ワークフローステップの設定モーダル](https://api.slack.com/reference/workflows/configuration-view)をビルダーに送信する必要があります。このモーダルは、そのステップ独自の設定を選択するための場所です。通常のモーダルより制限が強く、例えば `title`、`submit`、`close` のプロパティを含めることができません。設定モーダルの `callback_id` は、デフォルトではワークフローステップと同じものになります。

`edit` コールバック内で `configure()` ユーティリティを使用すると、対応する `blocks` 引数にビューのblocks 部分だけを渡して、ステップの設定モーダルを簡単に表示させることができます。必要な入力内容が揃うまで設定の保存を無効にするには、`True` の値をセットした `submit_disabled` を渡します。

設定モーダルの開き方に関する詳細は、[こちらのドキュメント](https://api.slack.com/workflows/steps#handle_config_view)を参照してください。

指定可能な引数の一覧はモジュールドキュメントを参考にしてください（<a href="https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html">共通</a> / <a href="https://tools.slack.dev/bolt-python/api-docs/slack_bolt/workflows/step/utilities/index.html">ステップ用</a>

```python
def edit(ack, step, configure):
    ack()

    blocks = [
        {
            "type": "input",
            "block_id": "task_name_input",
            "element": {
                "type": "plain_text_input",
                "action_id": "name",
                "placeholder": {"type": "plain_text", "text":"Add a task name"},
            },
            "label": {"type": "plain_text", "text":"Task name"},
        },
        {
            "type": "input",
            "block_id": "task_description_input",
            "element": {
                "type": "plain_text_input",
                "action_id": "description",
                "placeholder": {"type": "plain_text", "text":"Add a task description"},
            },
            "label": {"type": "plain_text", "text":"Task description"},
        },
    ]
    configure(blocks=blocks)

ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)
app.step(ws)
```

##  ステップの設定の保存

設定モーダルを開いた後、アプリは `view_submission` イベントをリッスンします。このイベントがアプリに届くと、`WorkflowStep` で設定した `save` コールバックが実行されます。

`save` コールバック内では、`update()` メソッドを使って、ワークフローに追加されたステップの設定を保存することができます。このメソッドには次の引数を指定します。

- `inputs` : ユーザーがワークフローステップを実行したときにアプリが受け取る予定のデータを表す辞書型の値です。
- `outputs` : ワークフローステップの完了時にアプリが出力するデータが設定されたオブジェクトのリストです。この outputs は、ワークフローの後続のステップで利用することができます。
- `step_name` : ステップのデフォルトの名前をオーバーライドします。
- `step_image_url` : ステップのデフォルトの画像をオーバーライドします。

これらのパラメータの構成方法に関する詳細は、[こちらのドキュメント](https://api.slack.com/reference/workflows/workflow_step)を参照してください。

指定可能な引数の一覧はモジュールドキュメントを参考にしてください（<a href="https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html">共通</a> / <a href="https://tools.slack.dev/bolt-python/api-docs/slack_bolt/workflows/step/utilities/index.html">ステップ用</a>

```python
def save(ack, view, update):
    ack()

    values = view["state"]["values"]
    task_name = values["task_name_input"]["name"]
    task_description = values["task_description_input"]["description"]

    inputs = {
        "task_name": {"value": task_name["value"]},
        "task_description": {"value": task_description["value"]}
    }
    outputs = [
        {
            "type": "text",
            "name": "task_name",
            "label":"Task name",
        },
        {
            "type": "text",
            "name": "task_description",
            "label":"Task description",
        }
    ]
    update(inputs=inputs, outputs=outputs)

ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)
app.step(ws)
```

## ステップの実行

エンドユーザーがワークフローステップを実行すると、アプリに [`workflow_step_execute` イベントが送信されます](https://api.slack.com/events/workflow_step_execute)。このイベントがアプリに届くと、`WorkflowStep` で設定した `execute` コールバックが実行されます。

`save` コールバックで取り出した `inputs` を使って、サードパーティの API を呼び出す、情報をデータベースに保存する、ユーザーのホームタブを更新するといった処理を実行することができます。また、ワークフローの後続のステップで利用する出力値を `outputs` オブジェクトに設定します。

`execute` コールバック内では、`complete()` を呼び出してステップの実行が成功したことを示すか、`fail()` を呼び出してステップの実行が失敗したことを示す必要があります。

<span>指定可能な引数の一覧はモジュールドキュメントを参考にしてください（<a href="https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html">共通</a> / <a href="https://tools.slack.dev/bolt-python/api-docs/slack_bolt/workflows/step/utilities/index.html">ステップ用</a>）</span>
```python
def execute(step, complete, fail):
    inputs = step["inputs"]
    # すべての処理が成功した場合
    outputs = {
        "task_name": inputs["task_name"]["value"],
        "task_description": inputs["task_description"]["value"],
    }
    complete(outputs=outputs)

    # 失敗した処理がある場合
    error = {"message":"Just testing step failure!"}
    fail(error=error)

ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)
app.step(ws)
```