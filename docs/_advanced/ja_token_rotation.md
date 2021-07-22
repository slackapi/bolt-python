---
title: トークンのローテーション
lang: ja-jp
slug: token-rotation
order: 6
---

<div class="section-content">
Bolt for Python [v1.7.0](https://github.com/slackapi/bolt-python/releases/tag/v1.7.0) より、[OAuth V2 RFC](https://datatracker.ietf.org/doc/html/rfc6749#section-10.4) で規定され、アクセストークンに対するセキュリティを強化する、トークンローテーションを提供しています。

既存の Slack app のアクセストークンが無期限に存在し続けるのに対し、トークンローテーションを有効にすると、アクセストークンは失効します。これに対し、リフレッシュトークンを用いて、長期にわたりアクセストークンの更新行います。

Bolt for Python は[組み込みの OAuth](https://slack.dev/bolt-python/concepts#authenticating-oauth) が使用されている場合、自動的にトークンローテーションを行います。

トークンローテーションについての詳細な情報は、この[ドキュメント](https://api.slack.com/authentication/rotation)をご覧ください。
</div>
