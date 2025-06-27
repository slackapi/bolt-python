---
title: エージェント・アシスタント
lang: en
slug: /concepts/assistant
---

このページは、Bolt を使ってエージェント・アシスタントを実装するための方法を紹介します。この機能に関する一般的な情報については、[こちらのドキュメントページ（英語）](https://docs.slack.dev/ai/)を参照してください。

この機能を実装するためには、まず[アプリの設定画面](https://api.slack.com/apps)で **Agents & Assistants** 機能を有効にし、**OAuth & Permissions** のページで [`assistant:write`](https://docs.slack.dev/reference/scopes/assistant.write)、[chat:write](https://docs.slack.dev/reference/scopes/chat.write)、[`im:history`](https://docs.slack.dev/reference/scopes/im.history) を**ボットの**スコープに追加し、**Event Subscriptions** のページで [`assistant_thread_started`](https://docs.slack.dev/reference/events/assistant_thread_started)、[`assistant_thread_context_changed`](https://docs.slack.dev/reference/events/assistant_thread_context_changed)、[`message.im`](https://docs.slack.dev/reference/events/message.im) イベントを有効にしてください。

また、この機能は Slack の有料プランでのみ利用可能です。もし開発用の有料プランのワークスペースをお持ちでない場合は、[Developer Program](https://api.slack.com/developer-program) に参加し、全ての有料プラン向け機能を利用可能なサンドボックス環境をつくることができます。

ユーザーとのアシスタントスレッド内でのやりとりを処理するには、`assistant_thread_started`、`assistant_thread_context_changed`、`message` イベントの `app.event(...)` リスナーを使うことも可能ですが、Bolt はよりシンプルなアプローチを提供しています。`Assistant` インスタンスを作り、それに必要なイベントリスナーを追加し、最後にこのアシスタント設定を `App` インスタンスに渡すだけでよいのです。

```python
assistant = Assistant()

# ユーザーがアシスタントスレッドを開いたときに呼び出されます
@assistant.thread_started
def start_assistant_thread(say: Say, set_suggested_prompts: SetSuggestedPrompts):
    # ユーザーに対して最初の返信を送信します
    say(":wave: Hi, how can I help you today?")

    # プロンプト例を送るのは必須ではありません
    set_suggested_prompts(
        prompts=[
            # もしプロンプトが長い場合は {"title": "表示する短いラベル", "message": "完全なプロンプト"} を使うことができます
            "What does SLACK stand for?",
            "When Slack was released?",
        ],
    )

# ユーザーがスレッド内で返信したときに呼び出されます
@assistant.user_message
def respond_in_assistant_thread(
    payload: dict,
    logger: logging.Logger,
    context: BoltContext,
    set_status: SetStatus,
    say: Say,
    client: WebClient,
):
    try:
        # ユーザーにこのbotがリクエストを受信して作業中であることを伝えます
        set_status("is typing...")

        # 会話の履歴を取得します
        replies_in_thread = client.conversations_replies(
            channel=context.channel_id,
            ts=context.thread_ts,
            oldest=context.thread_ts,
            limit=10,
        )
        messages_in_thread: List[Dict[str, str]] = []
        for message in replies_in_thread["messages"]:
            role = "user" if message.get("bot_id") is None else "assistant"
            messages_in_thread.append({"role": role, "content": message["text"]})

        # プロンプトと会話の履歴を LLM に渡します（この call_llm はあなた自身のコードです）
        returned_message = call_llm(messages_in_thread)

        # 結果をアシスタントスレッドに送信します
        say(text=returned_message)

    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")
        # エラーになった場合は必ずメッセージを送信するようにしてください
        # そうしなかった場合、'is typing...' の表示のままになってしまい、ユーザーは会話を続けることができなくなります
        say(f":warning: Sorry, something went wrong during processing your request (error: {e})")

# このミドルウェアを Bolt アプリに追加します
app.use(assistant)
```

<span>リスナーに指定可能な引数の一覧は<a href="https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html">モジュールドキュメント</a>を参考にしてください。</span>

ユーザーがチャンネルの横でアシスタントスレッドを開いた場合、そのチャンネルの情報は、そのスレッドの `AssistantThreadContext` データとして保持され、 `get_thread_context` ユーティリティを使ってアクセスすることができます。Bolt がこのユーティリティを提供している理由は、後続のユーザーメッセージ投稿のイベントペイロードに最新のスレッドのコンテキスト情報は含まれないためです。そのため、アプリはコンテキスト情報が変更されたタイミングでそれを何らかの方法で保存し、後続のメッセージイベントのリスナーコードから参照できるようにする必要があります。

そのユーザーがチャンネルを切り替えた場合、`assistant_thread_context_changed` イベントがあなたのアプリに送信されます。（上記のコード例のように）組み込みの `Assistant` ミドルウェアをカスタム設定なしで利用している場合、この更新されたチャンネル情報は、自動的にこのアシスタントボットからの最初の返信のメッセージメタデータとして保存されます。これは、組み込みの仕組みを使う場合は、このコンテキスト情報を自前で用意したデータストアに保存する必要はないということです。この組み込みの仕組みの唯一の短所は、追加の Slack API 呼び出しによる処理時間のオーバーヘッドです。具体的には `get_thread_context` を実行したときに、この保存されたメッセージメタデータにアクセスするために `conversations.history` API が呼び出されます。

このデータを別の場所に保存したい場合、自前の `AssistantThreadContextStore` 実装を `Assistant` のコンストラクターに渡すことができます。リファレンス実装として、`FileAssistantThreadContextStore` というローカルファイルシステムを使って実装を提供しています:

```python
# これはあくまで例であり、自前のものを渡すことができます
from slack_bolt import FileAssistantThreadContextStore
assistant = Assistant(thread_context_store=FileAssistantThreadContextStore())
```

このリファレンス実装はローカルファイルに依存しており、本番環境での利用は推奨しません。本番アプリでは `AssistantThreadContextStore` を継承した自前のクラスを使うようにしてください。

最後に、動作する完全なサンプルコード例を確認したい場合は、私たちが GitHub 上で提供している[サンプルアプリのリポジトリ](https://github.com/slack-samples/bolt-python-assistant-template)をチェックしてみてください。

## アシスタントスレッドでの Block Kit インタラクション

より高度なユースケースでは、上のようなプロンプト例の提案ではなく Block Kit のボタンなどを使いたいという場合があるかもしれません。そして、後続の処理のために[構造化されたメッセージメタデータ](https://docs.slack.dev/messaging/message-metadata/)を含むメッセージを送信したいという場合もあるでしょう。

例えば、アプリが最初の返信で「参照しているチャンネルを要約」のようなボタンを表示し、ユーザーがそれをクリックして、より詳細な情報（例：要約するメッセージ数・日数、要約の目的など）を送信、アプリがそれを構造化されたメータデータに整理した上でリクエスト内容をボットのメッセージとして送信するようなシナリオです。

デフォルトでは、アプリはそのアプリ自身から送信したボットメッセージに応答することはできません（Bolt にはあらかじめ無限ループを防止する制御が入っているため）。`ignoring_self_assistant_message_events_enabled=False` を `App` のコンストラクターに渡し、`bot_message` リスナーを `Assistant` ミドルウェアに追加すると、上記の例のようなリクエストを伝えるボットメッセージを使って処理を継続することができるようになります。

```python
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    # bot message を受け取るには必ずこれを指定してください
    ignoring_self_assistant_message_events_enabled=False,
)

assistant = Assistant()

# リスナーに指定可能な引数の一覧は https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html を参照してください

@assistant.thread_started
def start_assistant_thread(say: Say):
    say(
        text=":wave: Hi, how can I help you today?",
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": ":wave: Hi, how can I help you today?"},
            },
            {
                "type": "actions",
                "elements": [
                    # 複数のボタンを配置することが可能です
                    {
                        "type": "button",
                        "action_id": "assistant-generate-random-numbers",
                        "text": {"type": "plain_text", "text": "Generate random numbers"},
                        "value": "clicked",
                    },
                ],
            },
        ],
    )

# 上のボタンがクリックされたときに実行されます
@app.action("assistant-generate-random-numbers")
def configure_random_number_generation(ack: Ack, client: WebClient, body: dict):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "configure_assistant_summarize_channel",
            "title": {"type": "plain_text", "text": "My Assistant"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            # アシスタントスレッドの情報を app.view リスナーに引き継ぎます
            "private_metadata": json.dumps(
                {
                    "channel_id": body["channel"]["id"],
                    "thread_ts": body["message"]["thread_ts"],
                }
            ),
            "blocks": [
                {
                    "type": "input",
                    "block_id": "num",
                    "label": {"type": "plain_text", "text": "# of outputs"},
                    # 自然言語のテキストではなく、あらかじめ決められた形式の入力を受け取ることができます
                    "element": {
                        "type": "static_select",
                        "action_id": "input",
                        "placeholder": {"type": "plain_text", "text": "How many numbers do you need?"},
                        "options": [
                            {"text": {"type": "plain_text", "text": "5"}, "value": "5"},
                            {"text": {"type": "plain_text", "text": "10"}, "value": "10"},
                            {"text": {"type": "plain_text", "text": "20"}, "value": "20"},
                        ],
                        "initial_option": {"text": {"type": "plain_text", "text": "5"}, "value": "5"},
                    },
                }
            ],
        },
    )

# 上のモーダルが送信されたときに実行されます
@app.view("configure_assistant_summarize_channel")
def receive_random_number_generation_details(ack: Ack, client: WebClient, payload: dict):
    ack()
    num = payload["state"]["values"]["num"]["input"]["selected_option"]["value"]
    thread = json.loads(payload["private_metadata"])

    # 構造化された入力情報とともにボットのメッセージを送信します
    # 以下の assistant.bot_message リスナーが処理を継続します
    # このリスナー内で処理したい場合はそれでも構いません！
    # bot_message リスナーが必要ない場合は ignoring_self_assistant_message_events_enabled=False を設定する必要はありません
    client.chat_postMessage(
        channel=thread["channel_id"],
        thread_ts=thread["thread_ts"],
        text=f"OK, you need {num} numbers. I will generate it shortly!",
        metadata={
            "event_type": "assistant-generate-random-numbers",
            "event_payload": {"num": int(num)},
        },
    )

# このアプリのボットユーザーがメッセージを送信したときに実行されます
@assistant.bot_message
def respond_to_bot_messages(logger: logging.Logger, set_status: SetStatus, say: Say, payload: dict):
    try:
        if payload.get("metadata", {}).get("event_type") == "assistant-generate-random-numbers":
            # 上の random-number-generation リクエストを処理します
            set_status("is generating an array of random numbers...")
            time.sleep(1)
            nums: Set[str] = set()
            num = payload["metadata"]["event_payload"]["num"]
            while len(nums) < num:
                nums.add(str(random.randint(1, 100)))
            say(f"Here you are: {', '.join(nums)}")
        else:
            # それ以外のパターンでは何もしません
            # さらに他のパターンを追加する場合、メッセージ送信の無限ループを起こさないよう注意して実装してください
            pass

    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")

# ユーザーが返信したときに実行されます
@assistant.user_message
def respond_to_user_messages(logger: logging.Logger, set_status: SetStatus, say: Say):
    try:
        set_status("is typing...")
        say("Please use the buttons in the first reply instead :bow:")
    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")
        say(f":warning: Sorry, something went wrong during processing your request (error: {e})")

# このミドルウェアを Bolt アプリに追加します
app.use(assistant)
```