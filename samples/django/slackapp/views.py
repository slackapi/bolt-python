import logging
import os
from logging import Logger
from typing import Optional
from uuid import uuid4

from django.db.models import F
from django.db.models.functions import Coalesce
from django.http import HttpRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from slack_sdk.oauth import InstallationStore, OAuthStateStore
from slack_sdk.oauth.installation_store import Bot, Installation

from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings
from .models import SlackOAuthState, SlackBot, SlackInstallation


class DjangoInstallationStore(InstallationStore):
    client_id: str

    def __init__(
        self, client_id: str, logger: Logger,
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
        self, *, enterprise_id: Optional[str], team_id: Optional[str]
    ) -> Optional[Bot]:
        rows = (
            SlackBot.objects.filter(enterprise_id=enterprise_id)
            .filter(team_id=team_id)
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


class DjangoOAuthStateStore(OAuthStateStore):
    expiration_seconds: int

    def __init__(
        self, expiration_seconds: int, logger: Logger,
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


logger = logging.getLogger(__name__)
client_id, client_secret, signing_secret = (
    os.environ["SLACK_CLIENT_ID"],
    os.environ["SLACK_CLIENT_SECRET"],
    os.environ["SLACK_SIGNING_SECRET"],
)

app = App(
    signing_secret=signing_secret,
    installation_store=DjangoInstallationStore(client_id=client_id, logger=logger,),
    oauth_settings=OAuthSettings(
        client_id=client_id,
        client_secret=client_secret,
        state_store=DjangoOAuthStateStore(expiration_seconds=120, logger=logger,),
    ),
)


@app.event("app_mention")
def event_test(body, say, logger):
    logger.info(body)
    say("What's up?")


handler = SlackRequestHandler(app=app)


@csrf_exempt
def events(request: HttpRequest):
    return handler.handle(request)


def oauth(request: HttpRequest):
    return handler.handle(request)
