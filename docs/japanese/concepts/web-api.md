---
title: Web API の使い方
lang: ja-jp
slug: /ja-jp/bolt-python/concepts/web-api
---

`app.client`、またはミドルウェア・リスナーの引数 `client` として Bolt アプリに提供されている `WebClient` は必要な権限を付与されており、これを利用することで[あらゆる Web API メソッド](/reference/methods)を呼び出すことができます。このクライアントのメソッドを呼び出すと `SlackResponse` という Slack からの応答情報を含むオブジェクトが返されます。

Bolt の初期化に使用するトークンは `context` オブジェクトに設定されます。このトークンは、多くの Web API メソッドを呼び出す際に必要となります。

<span>指定可能な引数の一覧は<a href="https://docs.slack.dev/bolt-python/reference/kwargs_injection/args.html">モジュールドキュメント</a>を参考にしてください。</span>
```python
@app.message("wake me up")
def say_hello(client, message):
    # 2020 年 9 月 30 日午後 11:59:59 を示す Unix エポック秒
    when_september_ends = 1601510399
    channel_id = message["channel"]
    client.chat_scheduleMessage(
        channel=channel_id,
        post_at=when_september_ends,
        text="Summer has come and passed"
    )
```