from django.db import models


class SlackBot(models.Model):
    client_id = models.TextField(null=False)
    app_id = models.TextField(null=False)
    enterprise_id = models.TextField(null=True)
    team_id = models.TextField(null=True)
    bot_token = models.TextField(null=True)
    bot_id = models.TextField(null=True)
    bot_user_id = models.TextField(null=True)
    bot_scopes = models.TextField(null=True)
    installed_at = models.DateTimeField(null=False)

    class Meta:
        indexes = [
            models.Index(
                fields=["client_id", "enterprise_id", "team_id", "installed_at"]
            ),
        ]


class SlackInstallation(models.Model):
    client_id = models.TextField(null=False)
    app_id = models.TextField(null=False)
    enterprise_id = models.TextField(null=True)
    team_id = models.TextField(null=True)
    bot_token = models.TextField(null=True)
    bot_id = models.TextField(null=True)
    bot_user_id = models.TextField(null=True)
    bot_scopes = models.TextField(null=True)
    user_id = models.TextField(null=False)
    user_token = models.TextField(null=True)
    user_scopes = models.TextField(null=True)
    incoming_webhook_url = models.TextField(null=True)
    incoming_webhook_channel_id = models.TextField(null=True)
    incoming_webhook_configuration_url = models.TextField(null=True)
    installed_at = models.DateTimeField(null=False)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "client_id",
                    "enterprise_id",
                    "team_id",
                    "user_id",
                    "installed_at",
                ]
            ),
        ]


class SlackOAuthState(models.Model):
    state = models.TextField(null=False)
    expire_at = models.DateTimeField(null=False)
