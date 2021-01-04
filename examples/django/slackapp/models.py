# ----------------------
# Database tables
# ----------------------

from django.db import models


class SlackBot(models.Model):
    client_id = models.TextField(null=False)
    app_id = models.TextField(null=False)
    enterprise_id = models.TextField(null=True)
    enterprise_name = models.TextField(null=True)
    team_id = models.TextField(null=True)
    team_name = models.TextField(null=True)
    bot_token = models.TextField(null=True)
    bot_id = models.TextField(null=True)
    bot_user_id = models.TextField(null=True)
    bot_scopes = models.TextField(null=True)
    is_enterprise_install = models.BooleanField(null=True)
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
    enterprise_name = models.TextField(null=True)
    enterprise_url = models.TextField(null=True)
    team_id = models.TextField(null=True)
    team_name = models.TextField(null=True)
    bot_token = models.TextField(null=True)
    bot_id = models.TextField(null=True)
    bot_user_id = models.TextField(null=True)
    bot_scopes = models.TextField(null=True)
    user_id = models.TextField(null=False)
    user_token = models.TextField(null=True)
    user_scopes = models.TextField(null=True)
    incoming_webhook_url = models.TextField(null=True)
    incoming_webhook_channel = models.TextField(null=True)
    incoming_webhook_channel_id = models.TextField(null=True)
    incoming_webhook_configuration_url = models.TextField(null=True)
    is_enterprise_install = models.BooleanField(null=True)
    token_type = models.TextField(null=True)
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


# ----------------------
# Bolt store implementations
# ----------------------


from logging import Logger
from typing import Optional
from uuid import uuid4
from django.db.models import F
from django.utils import timezone
from slack_sdk.oauth import InstallationStore, OAuthStateStore
from slack_sdk.oauth.installation_store import Bot, Installation


class DjangoInstallationStore(InstallationStore):
    client_id: str

    def __init__(
        self,
        client_id: str,
        logger: Logger,
    ):
        self.client_id = client_id
        self._logger = logger

    @property
    def logger(self) -> Logger:
        return self._logger

    def save(self, installation: Installation):
        i = installation.to_dict()
        i["client_id"] = self.client_id
        SlackInstallation(**i).save()
        b = installation.to_bot().to_dict()
        b["client_id"] = self.client_id
        SlackBot(**b).save()

    def find_bot(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Bot]:
        e_id = enterprise_id or None
        t_id = team_id or None
        if is_enterprise_install:
            t_id = None
        rows = (
            SlackBot.objects.filter(enterprise_id=e_id)
            .filter(team_id=t_id)
            .order_by(F("installed_at").desc())[:1]
        )
        if len(rows) > 0:
            b = rows[0]
            return Bot(
                app_id=b.app_id,
                enterprise_id=b.enterprise_id,
                team_id=b.team_id,
                bot_token=b.bot_token,
                bot_id=b.bot_id,
                bot_user_id=b.bot_user_id,
                bot_scopes=b.bot_scopes,
                installed_at=b.installed_at.timestamp(),
            )
        return None

    def find_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: Optional[str] = None,
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Installation]:
        e_id = enterprise_id or None
        t_id = team_id or None
        if is_enterprise_install:
            t_id = None
        if user_id is None:
            rows = (
                SlackInstallation.objects.filter(enterprise_id=e_id)
                .filter(team_id=t_id)
                .order_by(F("installed_at").desc())[:1]
            )
        else:
            rows = (
                SlackInstallation.objects.filter(enterprise_id=e_id)
                .filter(team_id=t_id)
                .filter(user_id=user_id)
                .order_by(F("installed_at").desc())[:1]
            )

        if len(rows) > 0:
            i = rows[0]
            return Installation(
                app_id=i.app_id,
                enterprise_id=i.enterprise_id,
                team_id=i.team_id,
                bot_token=i.bot_token,
                bot_id=i.bot_id,
                bot_user_id=i.bot_user_id,
                bot_scopes=i.bot_scopes,
                user_id=i.user_id,
                user_token=i.user_token,
                user_scopes=i.user_scopes,
                incoming_webhook_url=i.incoming_webhook_url,
                incoming_webhook_channel_id=i.incoming_webhook_channel_id,
                incoming_webhook_configuration_url=i.incoming_webhook_configuration_url,
                installed_at=i.installed_at.timestamp(),
            )
        return None


class DjangoOAuthStateStore(OAuthStateStore):
    expiration_seconds: int

    def __init__(
        self,
        expiration_seconds: int,
        logger: Logger,
    ):
        self.expiration_seconds = expiration_seconds
        self._logger = logger

    @property
    def logger(self) -> Logger:
        return self._logger

    def issue(self) -> str:
        state: str = str(uuid4())
        expire_at = timezone.now() + timezone.timedelta(seconds=self.expiration_seconds)
        row = SlackOAuthState(state=state, expire_at=expire_at)
        row.save()
        return state

    def consume(self, state: str) -> bool:
        rows = SlackOAuthState.objects.filter(state=state).filter(
            expire_at__gte=timezone.now()
        )
        if len(rows) > 0:
            for row in rows:
                row.delete()
            return True
        return False


# ----------------------
# Slack App
# ----------------------

import logging
import os
from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings

logger = logging.getLogger(__name__)
client_id, client_secret, signing_secret = (
    os.environ["SLACK_CLIENT_ID"],
    os.environ["SLACK_CLIENT_SECRET"],
    os.environ["SLACK_SIGNING_SECRET"],
)

app = App(
    signing_secret=signing_secret,
    installation_store=DjangoInstallationStore(
        client_id=client_id,
        logger=logger,
    ),
    oauth_settings=OAuthSettings(
        client_id=client_id,
        client_secret=client_secret,
        state_store=DjangoOAuthStateStore(
            expiration_seconds=120,
            logger=logger,
        ),
    ),
)


@app.event("app_mention")
def event_test(body, say, logger):
    logger.info(body)
    say("What's up?")


@app.command("/hello-bolt-python")
def command(ack):
    ack("This is a Django app!")
