---
title: Lazy リスナー（FaaS）
lang: ja-jp
slug: lazy-listeners
order: 10
---

<div class="section-content">
⚠️ Lazy リスナー関数は、FaaS 環境への Bolt for Python アプリのデプロイを容易にする、ベータ版の機能です。開発中の機能であるため、Bolt for Python の API は変更される可能性があります。

通常、リスナー関数では最初の手順として `ack()` を呼び出します。`ack()` を呼び出すことで、アプリがリクエストを受け取り、適切な時間内（3 秒間）に処理する予定であることが Slack に伝えられます。

しかし、FaaS 環境や類似のランタイムで実行されるアプリでは、HTTP レスポンスを返したあとにスレッドやプロセスの実行を続けることができないため、同じパターンに従うことはできません。代わりに、`process_before_response` フラグを `True` に設定します。この設定により、`ack()` の呼び出しとリクエストの処理を安全に行うリスナーを作成することができます。しかし、3 秒以内にすべての処理を完了させる必要があることは変わりません。Events APIに応答するリスナーでは`ack()` メソッドの呼び出しを必要としませんが、この設定では処理を 3 秒以内に完了させる必要があります。

Lazy リスナーは、この問題を解決するためのソリューションです。Lazy リスナーは、デコレーターとして動作するものではなく、次の 2 つのキーワード引数を指定することにより動作するものです。 * `ack:Callable` : `ack()` の呼び出しを行います。 * `lazy:List[Callable]` : リクエストに関係する、時間のかかるプロセスの処理を担当します。Lazy 関数からは `ack()` にアクセスできません。
</div>

```python
def respond_to_slack_within_3_seconds(body, ack):
    text = body.get("text")
    if text is None or len(text) == 0:
        ack(f":x:Usage: /start-process (description here)")
    else:
        ack(f"Accepted! (task: {body['text']})")

import time
def run_long_process(respond, body):
    time.sleep(5)  # 3 秒より長い時間を指定します
    respond(f"Completed! (task: {body['text']})")

app.command("/start-process")(
    # この場合でも ack() は 3 秒以内に呼ばれます
    ack=respond_to_slack_within_3_seconds,
    # Lazy 関数がイベントの処理を担当します
    lazy=[run_long_process]
)
```

<details class="secondary-wrapper">
<summary class="section-head" markdown="0">
<h4 class="section-head">AWS Lambda を使用した例</h4>
</summary>

<div class="secondary-content" markdown="0">
このサンプルは、[AWS Lambda](https://aws.amazon.com/lambda/) にコードをデプロイします。[`examples` フォルダ](https://github.com/slackapi/bolt-python/tree/main/examples/aws_lambda)にはほかにもサンプルが用意されています。

```bash
pip install slack_bolt
# ソースコードを main.py として保存します
# config.yaml を設定してハンドラーを `handler: main.handler` で参照できるようにします

# https://pypi.org/project/python-lambda/
pip install python-lambda

# config.yml を適切に設定します
# lazy リスナーの実行には lambda:InvokeFunction と lambda:GetFunction が必要です
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***
echo 'slack_bolt' > requirements.txt
lambda deploy --config-file config.yaml --requirements requirements.txt
```
</div>

```python
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

# FaaS で実行するときは process_before_response を True にする必要があります
app = App(process_before_response=True)

def respond_to_slack_within_3_seconds(body, ack):
    text = body.get("text")
    if text is None or len(text) == 0:
        ack(":x: Usage: /start-process (description here)")
    else:
        ack(f"Accepted! (task: {body['text']})")

import time
def run_long_process(respond, body):
    time.sleep(5)  # 3 秒より長い時間を指定します
    respond(f"Completed! (task: {body['text']})")

app.command("/start-process")(
    ack=respond_to_slack_within_3_seconds,  # `ack()` の呼び出しを担当します
    lazy=[run_long_process]  # `ack()` の呼び出しはできません。複数の関数を持たせることができます。
)

def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
```

このサンプルアプリを実行するには、以下の IAM 権限が必要になります。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction",
                "lambda:GetFunction"
            ],
            "Resource": "*"
        }
    ]
}
```
</details>
